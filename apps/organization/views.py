from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from .models import CourseOrg, City
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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