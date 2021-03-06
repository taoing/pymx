from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.views.generic.base import View
from django.db.models import Q

from .models import CourseOrg, City, Teacher
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# 用django-pure-pagination实现分页
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course

'''
class OrgView(View):
    def get(self, request):
        # 所有课程机构
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        # 所有城市
        all_citys = City.objects.all()
        paginator = Paginator(all_orgs, 5)
        page = request.GET.get('page')
        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        context = {}
        context['all_orgs'] = page
        context['org_nums'] = org_nums
        context['all_citys'] = all_citys
        return render(request, 'org-list.html', context)
'''

class OrgView(View):
    def get(self, request):
        # 所有机构
        all_orgs = CourseOrg.objects.all()

        # 全部城市
        all_citys = City.objects.all()

        # 课程机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))

        # 获取用户选择的城市
        city_id = request.GET.get('city', '')
        # 如果选择了城市, 对城市的课程机构筛选
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 根据机构类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 根据机构的学生人数和课程数筛选排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            if sort == 'courses':
                all_orgs = all_orgs.order_by('-courses')

        # 机构数量
        org_nums = all_orgs.count()

        # 机构排名前三
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 对机构进行分页
        paginator = Paginator(all_orgs, 5, request=request)
        # 获取get请求url的查询参数, url中?之后就是查询参数
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
        context['all_orgs'] = page
        context['org_nums'] = org_nums
        context['all_citys'] = all_citys
        context['city_id'] = city_id
        context['category'] = category
        context['hot_orgs'] = hot_orgs
        context['sort'] = sort
        return render(request, 'org-list.html', context)

# 处理用户咨询, 响应ajax局部页面刷新请求, 返回json字符串
class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')

class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        course_org = get_object_or_404(CourseOrg, id=org_id)

        # get请求一次, click_nums +1
        course_org.click_nums += 1
        course_org.save()

        # 判断用户是否收藏机构
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 反向查询课程机构的所有课程和教师
        # 机构课程和教师较多时,应该限制机构主页显示数量,当前数据较少不做限制
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()
        context = {
            'current_page':current_page,
            'course_org':course_org,
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'has_fav':has_fav,
        }
        return render(request, 'org-detail-homepage.html', context)

class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = get_object_or_404(CourseOrg, id=org_id)
        # 判断用户是否收藏机构
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        context = {
            'current_page':current_page,
            'course_org':course_org,
            'all_courses':all_courses,
            'has_fav':has_fav,
        }
        return render(request, 'org-detail-course.html', context)

class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = get_object_or_404(CourseOrg, id=org_id)
        # 判断用户是否收藏机构
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        context = {
            'current_page':current_page,
            'course_org':course_org,
            'has_fav':has_fav,
        }
        return render(request, 'org-detail-desc.html', context)

class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = get_object_or_404(CourseOrg, id=org_id)
        # 判断用户是否收藏机构
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        context = {
            'current_page':current_page,
            'course_org':course_org,
            'all_teachers':all_teachers,
            'has_fav':has_fav,
        }
        return render(request, 'org-detail-teachers.html', context)

# 用户收藏, 取消收藏
class AddFavoriteView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='appliction/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        # 如果记录已存在, 表示操作要取消收藏, 取消收藏, 收藏数减1
        if exist_records:
            exist_records.delete()
            if fav_type == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                   course.fav_nums = 0
                course.save()
            elif fav_type == 2:
                course_org = Course_org.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif fav_type == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='appliction/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()

                # 收藏, 收藏数加1
                if fav_type == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif fav_type == 2:
                    course_org = Course_org.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='appliction/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='appliction/json')


class TeacherListView(View):
    '''
    授课教师列表
    '''
    def get(self, request):
        all_teachers = Teacher.objects.all()
        sorted_teachers = all_teachers.order_by('-click_nums')[:3]

        # 讲师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|
                                                Q(work_company__icontains=search_keywords)|
                                                Q(work_position__icontains=search_keywords)
                                                )

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
        else:
            sort = ''

        # 对教师分页
        paginator = Paginator(all_teachers, 3, request=request)
        # 获取get请求url的查询参数, url中?之后就是查询参数
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
        context['all_teachers'] = page
        context['sort'] = sort
        context['sorted_teachers'] = sorted_teachers
        return render(request, 'teachers-list.html', context)


class TeacherDetailView(View):
    '''
    教师详情
    '''
    def get(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)

        # 点击数加1
        teacher.click_nums += 1
        teacher.save()

        teacher_courses = teacher.course_set.all()

        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'teacher-detail.html', {
            'teacher':teacher,
            'teacher_courses':teacher_courses,
            'sorted_teachers':sorted_teachers,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
            })