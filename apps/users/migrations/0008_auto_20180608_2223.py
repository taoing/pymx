# Generated by Django 2.0.3 on 2018-06-08 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20180607_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='image/default.png', null=True, upload_to='image/%Y/%m', verbose_name='用户头像'),
        ),
    ]
