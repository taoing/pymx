from django.db import models

# Create your models here.

from datetime import datetime

class City(models.Model):
    name = models.CharField('城市', max_length = 20)
    add_time = models.DateTimeField('添加时间', default = datetime.now)

    def __str__(self):
        return self.name

class CourseOrg(models.Model):
    category_choices = (
        ('pxjg', '培训机构'),
        ('gx', '高校'),
        ('gr', '个人'),
        )

    name = models.CharField('机构名称', max_length = 40)
    city = models.ForeignKey(City, on_delete = models.CASCADE, null = True, blank = True, verbose_name = '所在城市')
    location = models.CharField('地址', max_length = 50)
    image = models.ImageField('logo', upload_to = 'org/%Y/%m', max_length = 100)
    desc = models.TextField('描述')
    add_time = models.DateTimeField('添加时间', default = datetime.now)
    index = models.IntegerField('排序', default = 999)
    click_nums = models.IntegerField('点击数', default = 0)
    fav_nums = models.IntegerField('收藏数', default = 0)
    has_auth = models.BooleanField('是否已认证', default = False)
    category = models.CharField('机构类别', max_length=10, choices=category_choices, default='pxjg')
    students = models.IntegerField('学生数', default=0)
    courses = models.IntegerField('课程数', default=0)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name

class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete = models.CASCADE, null = True, blank = True, verbose_name = '所属机构')
    name = models.CharField('姓名', max_length = 20)
    work_years = models.IntegerField('工作年限', default = 0)
    work_company = models.CharField('就职公司', max_length = 50)
    work_position = models.CharField('公司职位', max_length = 50)
    feature = models.CharField('教学特点', max_length = 300)
    click_nums = models.IntegerField('点击数', default = 0)
    fav_nums = models.IntegerField('收藏数', default = 0)
    add_time = models.DateTimeField('添加时间', default = datetime.now)
    image = models.ImageField('头像', upload_to = 'teacher/%Y/%m', max_length = 100, default='')
    age = models.IntegerField('年龄', default = 24)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name