from django.db import models

# Create your models here.
# 扩展django的默认用户系统
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pymx.settings import SECRET_KEY

class User(AbstractUser):
    gender_choices = (
        ('M', '男'),
        ('F', '女'),
    )

    nickname = models.CharField(verbose_name = '昵称', max_length = 50, null = True, blank = True)
    birthday = models.DateField(verbose_name = '生日', null = True, blank = True)
    gender = models.CharField(verbose_name = '性别', max_length = 1, choices = gender_choices, default = 'F')
    address  = models.CharField(verbose_name = '地址', max_length = 100, null = True, blank = True)
    email = models.EmailField('邮箱', max_length = 50)
    # upload_to选项来指定MEDIA_ROOT的一个子目录用于存放上传的文件, 数据库中存放的仅是这个文件的路径（相对于MEDIA_ROOT）
    image = models.ImageField(verbose_name='用户头像', upload_to = 'image/%Y/%m', default = 'image/default.png', max_length = 100, null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def str(self):
        return self.username

    def generate_activate_token(self, expiration=3600*24):
        s = Serializer(SECRET_KEY,expiration)
        return s.dumps({'activate':self.email}).decode('utf-8')

    def generate_reset_token(self, expiration=3600*24):
        s = Serializer(SECRET_KEY,expiration)
        return s.dumps({'reset':self.email}).decode('utf-8')

    def get_unread_nums(self):
        '''获取用户未读消息数量'''
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()

class EmailVerifyCode(models.Model):
    type_choices = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update_email','修改邮箱'),
        )

    email = models.EmailField(max_length = 50)
    verify_code = models.CharField('验证码', max_length = 20)
    send_type = models.CharField('验证码类型', choices = type_choices, max_length = 20)
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