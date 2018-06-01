# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField

#登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    password = forms.CharField(required=True, max_length=20, min_length=6)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, max_length=50)
    password = forms.CharField(required=True, min_length=6, max_length=20)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})

class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True, max_length=50)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})

class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)