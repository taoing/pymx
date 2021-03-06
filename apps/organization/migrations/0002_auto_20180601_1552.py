# Generated by Django 2.0.3 on 2018-06-01 15:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseorg',
            options={'verbose_name': '课程机构', 'verbose_name_plural': '课程机构'},
        ),
        migrations.AlterField(
            model_name='city',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=20, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='click_nums',
            field=models.IntegerField(default=0, verbose_name='点击数'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='desc',
            field=models.TextField(verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='fav_nums',
            field=models.IntegerField(default=0, verbose_name='收藏数'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(upload_to='org/%Y/%m', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='location',
            field=models.CharField(max_length=50, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='name',
            field=models.CharField(max_length=40, verbose_name='机构名称'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='click_nums',
            field=models.IntegerField(default=0, verbose_name='点击数'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='fav_nums',
            field=models.IntegerField(default=0, verbose_name='收藏数'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=20, verbose_name='姓名'),
        ),
    ]
