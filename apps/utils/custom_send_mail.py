# -*- coding: utf-8 -*-

#发送邮件是耗时操作,需要优化
from django.core.mail import send_mail
from django.urls import reverse

from pymx.settings import EMAIL_FROM

def send_register_email(email_to, token):
    subject = '注册激活链接'
    message = '请点击以下链接激活您的账户: http://127.0.0.1:8000%s' % reverse('activate', args=(token,))
    send_status = send_mail(subject, message, EMAIL_FROM, [email_to])
    if send_status:
        print('激活邮件已发送')
    else:
        print('邮件发送失败')

def send_reset_email(email_to, token):
    subject = '密码重置链接'
    message = '请点击以下链接重置您的密码: http://127.0.0.1:8000%s' % reverse('reset', args=(token,))
    send_status = send_mail(subject, message, EMAIL_FROM, [email_to])
    if send_status:
        print('密码重置邮件已发送')
    else:
        print('邮件发送失败')