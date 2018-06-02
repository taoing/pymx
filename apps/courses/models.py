from django.db import models

# Create your models here.

from datetime import datetime

from organization.models import CourseOrg

class Course(models.Model):
    name = models.CharField(max_length = 50, verbose_name = '课程名称')
    desc = models.CharField(max_length = 300, verbose_name = '课程描述')
    detail = models.TextField(verbose_name = '课程详情')
    degree = models.CharField(choices = (('cj', '初级'), ('zj', '中级'),('gj', '高级')), max_length = 2, verbose_name = '课程难度')
    learn_time = models.IntegerField(default = 0, verbose_name = '课程时长(分钟数)')
    students = models.IntegerField(default = 0, verbose_name = '学习人数')
    fav_nums = models.IntegerField(default = 0, verbose_name = '收藏人数')
    image = models.ImageField(upload_to = 'courese/%Y/%m', max_length = 100, verbose_name = '封面图')
    click_nums = models.IntegerField(default = 0, verbose_name = '点击数')
    add_time = models.DateTimeField(default = datetime.now, verbose_name = '添加时间')
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, null = True, blank = True, verbose_name = '课程')
    name = models.CharField('章节名', max_length = 100)
    add_time = models.DateTimeField('添加时间', default = datetime.now)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE, null = True, blank = True, verbose_name = '章节')
    name = models.CharField('视频名', max_length = 100)
    add_time = models.DateTimeField('添加时间', default = datetime.now)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, null = True, blank = True, verbose_name = '课程')
    name = models.CharField('资源名称', max_length = 100)
    add_time = models.DateTimeField('添加时间', default = datetime.now)
    download = models.FileField('资源文件', upload_to = 'course/resource/%Y/%m', max_length = 100)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name