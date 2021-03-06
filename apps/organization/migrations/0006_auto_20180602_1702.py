# Generated by Django 2.0.3 on 2018-06-02 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20180602_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': '教师', 'verbose_name_plural': '教师'},
        ),
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='头像'),
        ),
    ]
