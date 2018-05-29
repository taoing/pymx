# Generated by Django 2.0.3 on 2018-05-29 14:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('location', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='org/%Y/%m')),
                ('desc', models.TextField()),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
                ('index', models.IntegerField(default=999, verbose_name='排序')),
                ('click_nums', models.IntegerField(default=0)),
                ('fav_nums', models.IntegerField(default=0)),
                ('has_auth', models.BooleanField(default=False, verbose_name='是否已认证')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.City', verbose_name='所在城市')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('work_years', models.IntegerField(default=0, verbose_name='工作年限')),
                ('work_company', models.CharField(max_length=50, verbose_name='就职公司')),
                ('work_position', models.CharField(max_length=50, verbose_name='公司职位')),
                ('feature', models.CharField(max_length=300, verbose_name='教学特点')),
                ('click_nums', models.IntegerField(default=0)),
                ('fav_nums', models.IntegerField(default=0)),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.CourseOrg', verbose_name='所属机构')),
            ],
        ),
    ]
