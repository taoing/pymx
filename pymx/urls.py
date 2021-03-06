"""pymx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import xadmin
from django.views.static import serve

from users import views
from organization.views import OrgView
from pymx.settings import MEDIA_ROOT #, STATIC_ROOT

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    # path('login/', views.user_login, name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('captcha/', include('captcha.urls')),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<str:token>/', views.ActivateView.as_view(), name='activate'),
    path('forgetpwd/', views.ForgetPwdView.as_view(), name='forgetpwd'),
    path('reset/<str:token>/', views.ResetView.as_view(), name='reset'),
    path('resetpwd/', views.ResetPwdView.as_view(), name='resetpwd'),

    # 配置上传文件访问处理函数,启用django.views.static.server
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),

    #课程机构
    # path('org_list/', OrgView.as_view(), name='org_list'),
    path('org/', include('organization.urls', namespace='org')),

    #课程相关
    path('course/', include('courses.urls', namespace='course')),

    # 用户个人中心相关
    path('users/', include('users.urls', namespace='users')),

    # 富文本编辑器, 启用ckeditor_uploader时配置
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # DEBUG = False时, 静态文件访问处理
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root':STATIC_ROOT}),
]

#全局404错误页面配置
handler404 = 'users.views.custom_page_not_found'

#全局500错误页面配置
handler500 = 'users.views.server_error'