# Generated by Django 2.0.3 on 2018-06-02 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20180602_1541'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseresource',
            options={'verbose_name': '课程资源', 'verbose_name_plural': '课程资源'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': '章节', 'verbose_name_plural': '章节'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': '视频', 'verbose_name_plural': '视频'},
        ),
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='所属机构'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='video',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Lesson', verbose_name='章节'),
        ),
    ]
