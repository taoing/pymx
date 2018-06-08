# -*- coding: utf-8 -*-

#发送邮件是耗时操作,需要优化
import random

from django.core.mail import send_mail
from django.urls import reverse

from pymx.settings import EMAIL_FROM
from users.models import EmailVerifyCode

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

def random_str(code_length=6):
    '''
    随机生成邮箱验证码
    '''
    alist = ['0','1','2','3','4','5','6','7','8','9']
    # 根据ascii码将数字转换为大写字母
    for i in range(65,91):
        alist.append(chr(i))

    # 打乱alist的顺序
    random.shuffle(alist)

    code_list = random.sample(alist, code_length)
    code = ''.join(code_list)
    return code

def send_code_email(email_to):
    code = random_str()
    email_code = EmailVerifyCode()
    email_code.email = email_to
    email_code.verify_code = code
    email_code.send_type = 'update_email'
    email_code.save()

    subject = '邮箱修改验证码'
    message = '您的邮箱验证码为: {0}, 验证码在20分钟内有效'.format(code)
    send_status = send_mail(subject, message, EMAIL_FROM, [email_to])
    if send_status:
        print('验证码邮件已发送')
    else:
        print('邮件发送失败')