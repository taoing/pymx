# Generated by Django 2.0.3 on 2018-06-09 22:22

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_auto_20180609_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='描述'),
        ),
    ]