# -*- coding: utf-8 -*-

from django.urls import path, re_path

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView

# app的name
app_name = 'org'

urlpatterns = [
    path('list', OrgView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    path('org_home/<int:org_id>/', OrgHomeView.as_view(), name='org_home'),
    path('org_course/<int:org_id>/', OrgCourseView.as_view(), name='org_course'),
    path('org_desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
    path('org_teacher/<int:org_id>/', OrgTeacherView.as_view(), name='org_teacher'),
    ]