from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from .models import CourseOrg, City
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# 用django-pure-pagination实现分页
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

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
        page = request.GET.get('page')
        if page == None:
            page = 1
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