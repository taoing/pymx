# -*- coding: utf-8 -*-

from django import forms

#登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    password = forms.CharField(required=True, max_length=20, min_length=8)