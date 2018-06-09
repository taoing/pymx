# Generated by Django 2.0.3 on 2018-06-09 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_courseorg_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='org/%Y/%m', verbose_name='logo'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='teacher/%Y/%m', verbose_name='头像'),
        ),
    ]