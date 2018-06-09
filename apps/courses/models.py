from django.db import models

# Create your models here.

from datetime import datetime

# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from organization.models import CourseOrg, Teacher

class Course(models.Model):
    name = models.CharField(max_length = 50, verbose_name = '课程名称')
    desc = models.CharField(max_length = 300, verbose_name = '课程描述')
    # detail = models.TextField(verbose_name = '课程详情')
    # detail = RichTextField(verbose_name = '课程详情')
    detail = RichTextUploadingField(verbose_name = '课程详情')
    degree = models.CharField(choices = (('cj', '初级'), ('zj', '中级'),('gj', '高级')), max_length = 2, verbose_name = '课程难度')
    learn_time = models.IntegerField(default = 0, verbose_name = '课程时长(分钟数)')
    students = models.IntegerField(default = 0, verbose_name = '学习人数')
    fav_nums = models.IntegerField(default = 0, verbose_name = '收藏人数')
    image = models.ImageField(upload_to = 'courese/%Y/%m', max_length = 100, verbose_name = '封面图', null=True, blank=True)
    click_nums = models.IntegerField(default = 0, verbose_name = '点击数')
    add_time = models.DateTimeField(default = datetime.now, verbose_name = '添加时间')
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')
    category = models.CharField(default='', max_length = 20, verbose_name = '课程类别')
    tag = models.CharField(default='', max_length = 10, verbose_name = '课程标签')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, verbose_name='讲师')
    youneed_know = models.CharField('课程须知', max_length=300, null=True, blank=True)
    teacher_tell = models.CharField('讲师告知', max_length=300, null=True, blank=True)
    is_banner = models.BooleanField('是否轮播', default=False)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_lesson_nums(self):
        return self.lesson_set.all().count()
    get_lesson_nums.short_description = '章节数'

    def get_course_lesson(self):
        # 获取课程章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name

    def go_to(self):
        '''跳转到课程的详情页, 可以使用reverse解析url'''
        from django.utils.safestring import mark_safe
        # mark_safe标记字符串为安全字符串, 不需要html转义
        return mark_safe('<a href="/course/detail/%s/">跳转</a>' % self.id)
    go_to.short_description = '跳转'

class BannerCourse(Course):
    '''轮播课程'''
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        # 设置为代理模型, 共用同一张表, 可以在代理模型中有不同的展示逻辑
        proxy = True

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, null = True, blank = True, verbose_name = '课程')
    name = models.CharField('章节名', max_length = 100)
    add_time = models.DateTimeField('添加时间', default = datetime.now)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()

    def __str__(self):
        return self.name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE, null = True, blank = True, verbose_name = '章节')
    name = models.CharField('视频名', max_length = 100)
    url = models.CharField('视频地址', max_length=200, null=True, blank=True)
    learn_time = models.IntegerField('学习时长(分钟数)', default=0)
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