# Generated by Django 2.0.3 on 2018-06-09 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180608_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='banner/%Y/%m', verbose_name='轮播图'),
        ),
    ]
