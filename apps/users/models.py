from django.db import models

# Create your models here.
# 扩展django的默认用户系统
from datetime import datetime

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    gender_choices = (
        ('M', '男'),
        ('F', '女'),
    )

    nickname = models.CharField(max_length = 50, null = True, blank = True)
    birthday = models.DateField(verbose_name = '生日', null = True, blank = True)
    gender = models.CharField(verbose_name = '性别', max_length = 1, choices = gender_choices, default = 'F')
    address  = models.CharField(max_length = 100, null = True, blank = True)
    mobile = models.CharField('手机号', max_length = 11, null = True, blank = True)
    # upload_to选项来指定MEDIA_ROOT的一个子目录用于存放上传的文件, 数据库中存放的仅是这个文件的路径（相对于MEDIA_ROOT）
    image = models.ImageField(upload_to = 'image/%Y/%M', default = 'image/default.png', max_length = 100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def str(self):
        return self.username

class EmailVerifyCode(models.Model):
    type_choices = (
        ('register', '注册'),
        ('forget', '找回密码'),
        )

    email = models.EmailField(max_length = 50)
    verify_code = models.CharField('验证码', max_length = 20)
    send_type = models.CharField('验证码类型', choices = type_choices, max_length = 10)
    send_time = models.DateTimeField('发送时间', default = datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

class Banner(models.Model):
    title = models.CharField('标题', max_length = 100)
    image = models.ImageField('轮播图', upload_to = 'banner/%Y/%m', max_length = 100)
    url = models.URLField('链接', max_length = 200)
    index = models.IntegerField('顺序', default = 100)
    add_time = models.DateTimeField('添加时间', default = datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name