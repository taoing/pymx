from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.base import View
from .models import Course, CourseResource
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from operation.models import UserFavorite, CourseComment

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


class CourseDetailView(View):
    '''
    课程详情
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        # 课程点击数 +1
        course.click_nums += 1
        course.save()

        # 收藏
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org_id, fav_type=2):
                has_fav_org = True

        # 通过课程标签查找数据库中的课程
        tag = course.tag
        if tag:
            # 需做筛选, 防止推荐自己
            related_courses = Course.objects.filter(tag = tag)[:3]
        else:
            related_courses = []
        context = {}
        context['course'] = course
        context['related_courses'] = related_courses
        context['has_fav_course'] = has_fav_course
        context['has_fav_org'] = has_fav_org
        return render(request, 'course-detail.html', context)


class CourseInfoView(View):
    '''
    课程章节信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_resources = CourseResource.objects.filter(course=course)

        context = {}
        context['course'] = course
        context['all_resources'] = all_resources
        return render(request, 'course-video.html', context)

class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = course.coursecomment_set.all()
        context = {}
        context['course'] = course
        context['all_resources'] = all_resources
        context['all_comments'] = all_comments
        return render(request, 'course-comment.html', context)


class AddCommentView(View):
    '''
    用户评论, ajax发送post请求
    '''
    def post(self, request):
        # 未登录返回json提示未登录
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id)>0 and comments:
            course_comment = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comment.user = request.user
            course_comment.course = course
            course_comment.comments = comments
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论出错"}', content_type='application/json')