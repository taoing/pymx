# Generated by Django 2.0.3 on 2018-05-29 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180529_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]