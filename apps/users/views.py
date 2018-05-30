from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend #默认用户认证后端
from django.db.models import Q
from django.views.generic.base import View #基于类的视图

from .models import User
from .forms import LoginForm

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
                # login登录用户,将用户ID存入session中
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg':'用户名或密码错误', 'login_form':login_form})
        else:
            return render(request, 'login.html', {'login_form':login_form})

def user_logout(request):
    logout(request)
    return render(request, 'index.html')