# -*- coding: utf-8 -*-

import xadmin
from .models import EmailVerifyCode, Banner

from xadmin import views

# xadmin这里继承object, 不是admin.ModelAdmin
class EmailVerifyCodeAdmin(object):
    # 显示字段
    list_display = ['email', 'verify_code', 'send_type', 'send_time']
    # 搜索字段
    search_fields = ['email', 'verify_code', 'send_type']
    # 过滤字段
    list_filter = ['email', 'verify_code', 'send_type', 'send_time']

xadmin.site.register(EmailVerifyCode, EmailVerifyCodeAdmin)

class BannerAdmin(object):
    list_display = ('title', 'image', 'url', 'index', 'add_time')
    search_fields = ('title', 'image', 'url', 'index')
    list_filter = ('title', 'image', 'url', 'index', 'add_time')

xadmin.site.register(Banner, BannerAdmin)

# 创建xadmin最基本的管理器配置
class BaseSetting(object):
    #开启主题功能
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

# 全局修改, 固定写法 (修改管理网站标题和页脚)
class GlobalSettings(object):
    # 修改title
    site_title = '网站管理后台'
    # 修稿footer
    site_footer = 'pymx-allen'
    # 收起菜单
    menu_style = 'accordion'

xadmin.site.register(views.CommAdminView, GlobalSettings)