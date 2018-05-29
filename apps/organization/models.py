from django.db import models

# Create your models here.

from datetime import datetime

class City(models.Model):
    name = models.CharField(max_length = 20)
    add_time = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return self.name

class CourseOrg(models.Model):
    name = models.CharField(max_length = 40)
    city = models.ForeignKey(City, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = '所在城市')
    location = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = 'org/%Y/%m', max_length = 100)
    desc = models.TextField()
    add_time = models.DateTimeField(default = datetime.now)
    index = models.IntegerField('排序', default = 999)
    click_nums = models.IntegerField(default = 0)
    fav_nums = models.IntegerField(default = 0)
    has_auth = models.BooleanField('是否已认证', default = False)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = '所属机构')
    name = models.CharField(max_length = 20)
    work_years = models.IntegerField('工作年限', default = 0)
    work_company = models.CharField('就职公司', max_length = 50)
    work_position = models.CharField('公司职位', max_length = 50)
    feature = models.CharField('教学特点', max_length = 300)
    click_nums = models.IntegerField(default = 0)
    fav_nums = models.IntegerField(default = 0)
    add_time = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return self.name