from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend #默认用户认证后端
from django.db.models import Q
from django.views.generic.base import View #基于类的视图
from django.contrib.auth.hashers import make_password

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from pymx.settings import SECRET_KEY
from .models import User
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm
from utils.custom_send_mail import send_register_email, send_reset_email

# 自定义认证后端, 实现用户名和邮箱都可以登录,主要自定义实现authenticate和get_user方法, 这里只实现authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        #使用Q对象进行or查询
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            # check_password方法验证明文密码
            if user.check_password(password):
                return user
        except Exception as e:
            return None

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # authenticate在数据库中验证用户, 找到对应user,返回user对象,没找到返回None
        user = authenticate(username=username, password=password)
        if user is not None:
            # login登录用户,将用户ID存入session中
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg':'用户名或密码错误'})
    elif request.method == 'GET':
        return render(request, 'login.html')

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form':login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid(): # 验证表单数据
            username = login_form.cleaned_data.get('username', None)
            password = login_form.cleaned_data.get('password', None)
            user = authenticate(username=username, password=password)
            if user is not None:
                # 只有激活用户才能登录
                if user.is_active:
                    # login登录用户,将用户ID存入session中
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg':'请先去邮箱激活账户', 'login_form':login_form})
            else:
                return render(request, 'login.html', {'msg':'用户名或密码错误', 'login_form':login_form})
        else:
            return render(request, 'login.html', {'login_form':login_form})

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password')
            user = User.objects.filter(email=email)
            if user:
                return render(request, 'register.html', {'register_form':register_form, 'msg':'用户已存在'})
            user = User()
            user.email = email
            user.username = email.split('@',1)[0]
            user.password = make_password(password)
            user.is_active = False
            user.save()
            token = user.generate_activate_token()
            # 发送邮件耗时操作
            send_register_email(user.email, token)
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form':register_form})

# 账户激活
class ActivateView(View):
    def get(self, request, token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return render(request, 'activate_fail.html')
        email = date.get('activate')
        uesr = User.objects.filter(email=email)[0]
        if user:
            user.is_active = True
            user.save()
        else:
            return render(request, 'activate_fail.html')
        return render(request, 'login.html')

# 忘记密码,申请重置密码
class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form':forgetpwd_form})
    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = forgetpwd_form.cleaned_data.get('email')
            user = User.objects.filter(email=email)[0]
            if user:
                token = user.generate_reset_token()
                # 发送邮件耗时操作
                send_reset_email(user.email, token)
                return render(request, 'send_success.html')
        return render(request, 'forgetpwd.html', {'forgetpwd_form':forgetpwd_form})

# 验证密码重置链接
class ResetView(View):
    def get(self, request, token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return render(request, 'activate_fail.html')
        email = data.get('reset')
        user = User.objects.filter(email=email)[0]
        if user:
            return render(request, 'password_reset.html', {'email':email})
        return render(request, 'activate_fail.html')

# 重置密码
class ResetPwdView(View):
    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        email = request.POST.get('email')
        if resetpwd_form.is_valid():
            password1 = resetpwd_form.cleaned_data.get('password1')
            password2 = resetpwd_form.cleaned_data.get('password2')
            if password1 != password2:
                return render(request, 'password_reset.html', {'emial':email, 'resetpwd_form':resetpwd_form, 'msg':'密码不一致'})
            user = User.objects.filter(email=email)[0]
            user.password = make_password(password1)
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {'emial':email, 'resetpwd_form':resetpwd_form})


def user_logout(request):
    logout(request)
    return render(request, 'index.html')