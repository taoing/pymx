from django.shortcuts import render

# Create your views here.

import json
from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend #默认用户认证后端
from django.db.models import Q
from django.views.generic.base import View #基于类的视图
from django.contrib.auth.hashers import make_password

from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from pymx.settings import SECRET_KEY
from .models import User, EmailVerifyCode, Banner
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UploadImageForm, UserInfoForm
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course

from utils.custom_send_mail import send_register_email, send_reset_email, send_code_email
from utils.mixin_utils import LoginRequiredMixin

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


class IndexView(View):
    '''网站首页'''
    def get(self, request):
        banners = Banner.objects.all().order_by('index')[:3]

        courses = Course.objects.filter(is_banner=False)[:6]

        banner_courses = Course.objects.filter(is_banner=True)[:2]

        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'banners':banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,
        })

'''
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
'''

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
                    return HttpResponseRedirect(reverse('index'))
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
            user.username = email
            user.password = make_password(password)
            user.is_active = False
            user.save()

            # 向用户发送消息
            message = UserMessage()
            message.user = user.id
            message.message = '欢迎注册'
            message.save()

            token = user.generate_activate_token()
            # 发送邮件耗时操作
            send_register_email(user.email, token)
            return HttpResponseRedirect(reverse('login'))
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
            # 向用户发送消息
            message = UserMessage()
            message.user = user.id
            message.message = '账户已激活'
            message.save()
        else:
            return render(request, 'activate_fail.html')
        return HttpResponseRedirect(reverse('login'))

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

            # 向用户发送消息
            message = UserMessage()
            message.user = user.id
            message.message = '密码已重置'
            message.save()

            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'password_reset.html', {'emial':email, 'resetpwd_form':resetpwd_form})


'''
def user_logout(request):
    logout(request)
    return render(request, 'index.html')
'''

class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class UserInfoView(LoginRequiredMixin, View):
    '''
    用户个人信息
    '''
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    # 修改个人信息
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class UploadImageView(LoginRequiredMixin, View):
    '''
    用户图像修改
    '''
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class UpdatePwdView(LoginRequiredMixin, View):
    '''
    用户个人中心修改密码
    '''
    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            password1 = resetpwd_form.cleaned_data.get('password1')
            password2 = resetpwd_form.cleaned_data.get('password2')
            if password1 != password2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            request.user.password = make_password(password1)
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(resetpwd_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    '''
    发送邮箱修改验证码
    '''
    def get(self, request):
        email = request.GET.get('email')
        if User.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_code_email(email)
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''
    修改邮箱
    '''
    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')
        existed_code = EmailVerifyCode.objects.filter(email=email, verify_code=code)

        # 验证码有效时间20分钟
        if existed_code and (datetime.now() < existed_code[0].send_time + timedelta(seconds=20*60)):
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    '''我的课程'''
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses':user_courses,
            })


class MyFavOrgView(LoginRequiredMixin, View):
    ''''用户收藏的课程机构'''
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list':org_list,
            })


class MyFavTeacherView(LoginRequiredMixin, View):
    ''''用户收藏的授课教师'''
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list':teacher_list,
            })


class MyFavCourseView(LoginRequiredMixin, View):
    ''''用户收藏的公开课程'''
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list,
            })


class MyMessageView(LoginRequiredMixin, View):
    '''用户消息'''
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')

        # 所有未读消息变为已读
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 分页
        paginator = Paginator(all_messages, 2, request=request)
        page = request.GET.get('page', 1)
        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return render(request, 'usercenter-message.html', {
            'all_messages':page,
            })


def custom_page_not_found(request, exception):
    '''404错误页面, 自写404处理视图, 需调用默认的404的page_not_found视图函数'''
    from django.views.defaults import page_not_found
    res = page_not_found(request, exception, template_name='404.html')
    return res

def server_error(request):
    '''500错误页面, 505处理视图直接写'''
    return render(request, '500.html', status=500)