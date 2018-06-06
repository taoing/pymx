from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.base import View
from django.db.models import Q # 适用Q对象完成并查询

from .models import Course, CourseResource, Video
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin_utils import LoginRequiredMixin

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 课程搜索
        # 获取搜索关键词
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 用关键词在数据库中查找
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(detail__icontains=search_keywords))

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


class CourseInfoView(LoginRequiredMixin, View):
    '''
    课程章节信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        #查询用户是否学习了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            # 如果用户没有学习这门课程就将用户与课程关联起来, 创建usercourse记录
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        all_resources = CourseResource.objects.filter(course=course)

        # 学过该课程的用户, 还学过的其他课程
        # 该课程的所有usercourse记录
        user_courses = UserCourse.objects.filter(course=course)
        # 学过该课程的所有用户id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过所有用户id找到他们学习过的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 按课程点击量取前五, 现在数据较少,取一个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:2]

        context = {}
        context['course'] = course
        context['all_resources'] = all_resources
        context['relate_courses'] = relate_courses
        return render(request, 'course-video.html', context)

class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        #查询用户是否学习了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            # 如果用户没有学习这门课程就将用户与课程关联起来, 创建usercourse记录
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        all_resources = CourseResource.objects.filter(course=course)
        all_comments = course.coursecomment_set.all()

        # 学过该课程的用户, 还学过的其他课程
        # 该课程的所有usercourse记录
        user_courses = UserCourse.objects.filter(course=course)
        # 学过该课程的所有用户id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过所有用户id找到他们学习过的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 按课程点击量取前五, 现在数据较少,取一个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:2]

        context = {}
        context['course'] = course
        context['all_resources'] = all_resources
        context['all_comments'] = all_comments
        context['relate_courses'] = relate_courses
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

"""
不适用本地视频播放界面, 直接在课程章节界面跳转到慕课网站
class VideoPlayView(View):
    '''
    视频播放
    '''
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course

        all_resources = CourseResource.objects.filter(course=course)

        # 学过该课程的用户, 还学过的其他课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course_id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:2]

        context = {}
        context['video'] = video
        context['course'] = course
        context['all_resources'] = all_resources
        context['relate_courses'] = relate_courses
        return render(request, 'course-play.html', context)
"""