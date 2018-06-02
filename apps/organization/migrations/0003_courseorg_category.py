# Generated by Django 2.0.3 on 2018-06-01 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20180601_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')], default='pxjg', max_length=10, verbose_name='机构类别'),
        ),
    ]