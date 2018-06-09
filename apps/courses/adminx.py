# -*- coding: utf-8 -*-

import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse

class LessonInline(object):
    model = Lesson
    extra = 1

class CourseResourceInline(object):
    model = CourseResource
    extra = 1

class CourseAdmin(object):
    '''课程'''
    list_display = ('name','desc','detail','degree','learn_time','students', 'click_nums','get_lesson_nums', 'go_to') #列表页显示字段
    search_fields = ('name','desc','detail','degree','students') # 搜索字段
    list_filter = ('name','desc','detail','degree','learn_time','students') #过滤字段

    model_icon = 'fa fa-book' #图标
    ordering = ('-click_nums',) #排序
    readonly_fields = ('click_nums',) #制度字段
    exclude = ('fav_nums',) #不显示字段
    # 在列表页可以直接修改的字段
    list_editable = ('desc', 'degree')
    # 自动刷新, 可选的刷新时间
    refresh_times = (5, 10)

    inlines = [LessonInline, CourseResourceInline] #在课程更改页面内联显示章节和课程资源表单

    def queryset(self):
        '''重写模型的queryset方法, 过滤我们想要的数据'''
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        '''重写在管理后台中保存对象时的方法, 实现在保存对象时, 实现其他操作'''
        obj = self.new_obj
        obj.save()
        if obj.course_org:
            course_org = obj.course_org
            # 课程保存后, 课程机构的课程数要刷新
            course_org.courses = course_org.course_set.all().count()
            course_org.save()


class BannerCourseAdmin(object):
    '''轮播课程'''
    list_display = ('name','desc','detail','degree','learn_time','students', 'click_nums') #列表页显示字段
    search_fields = ('name','desc','detail','degree','students') # 搜索字段
    list_filter = ('name','desc','detail','degree','learn_time','students') #过滤字段

    model_icon = 'fa fa-book' #图标
    ordering = ('-click_nums',) #排序
    readonly_fields = ('click_nums',) #制度字段
    exclude = ('fav_nums',) #不显示字段

    inlines = [LessonInline, CourseResourceInline] #在课程更改页面内联显示章节和课程资源表单

    def queryset(self):
        '''重写模型的queryset方法, 过滤我们想要的数据'''
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ('course', 'name', 'add_time')
    search_fields = ('course', 'name')
    #根据课程名称进行过滤
    list_filter = ('course__name', 'name', 'add_time')

class VideoAdmin(object):
    list_display = ('lesson', 'name', 'add_time')
    search_fields = ('lesson', 'name')
    list_filter = ('lesson', 'name', 'add_time')

class CourseResourceAdmin(object):
    list_display = ('course','name','add_time','download')
    search_fields = ('course','name','download')
    list_filter = ('course__name','name','add_time','download')

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)