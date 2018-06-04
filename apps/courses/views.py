from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from .models import Course
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'students':
                all_courses = all_courses.order_by('students')

        # 分页
        paginator = Paginator(all_courses, 3, request=request)
        page = request.GET.get('page', 1)
        try:
            page = paginator.page(page)
        # page不是整数
        except PageNotAnInteger:
            page = paginator.page(1)
        # page超出了页码范围,获取最后一页
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context = {}
        context['all_courses'] = page
        context['hot_courses'] = hot_courses
        context['sort'] = sort
        return render(request, 'course-list.html', context)