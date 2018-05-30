# -*- coding: utf-8 -*-

import xadmin

from .models import City, CourseOrg, Teacher

class CityAdmin(object):
    list_display = ('name','add_time')
    search_fields = ('name',)
    list_filter = ('name','add_time')

class CourseOrgAdmin(object):
    list_display = ('name','desc','click_nums','fav_nums','add_time')
    search_fields = ('name','desc','click_nums','fav_nums')
    list_filter = ('name','desc','click_nums','fav_nums','city__name','add_time')

class TeacherAdmin(object):
    list_display = ('name','org','work_years','work_company','add_time')
    search_fields = ('name','org','work_years','work_company','add_time')
    list_filter = ('org__name','name','work_years','work_company','click_nums','fav_nums','add_time')

xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)