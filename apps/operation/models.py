from django.db import models

# Create your models here.
from datetime import datetime

from users.models import User
from courses.models import Course

# 用户咨询
class UserAsk(models.Model):
    name = models.CharField('用户姓名', max_length=20)
    mobile = models.CharField('手机号', max_length=11)
    course_name = models.CharField('课程名称', max_length=50)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

# 用户课程评论
class CourseComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    comments = models.CharField(max_length=200)
    add_time = models.DateTimeField(default=datetime.now)

# 用户收藏
class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fav_id = models.IntegerField('数据ID', default=0)
    fav_type = models.IntegerField(choices=((1,'课程'),(2,'课程机构'),(3,'讲师')), default=1)
    add_time = models.DateTimeField(default=datetime.now)

# 用户消息
class UserMessage(models.Model):
    user = models.IntegerField('用户', default=0)
    message = models.CharField('消息内容', max_length=500)
    has_read = models.BooleanField('消息是否已读', default=False)
    add_time = models.DateTimeField(default=datetime.now)

# 用户课程
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now)