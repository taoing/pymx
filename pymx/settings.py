"""
Django settings for pymx project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 将apps目录加入django的搜索目录中, 应用的包搜索目录默认是sys.path,这是一个路径列表,将apps的目录插入到sys.path中即可
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# 添加xadmin搜索路径支持
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jiq$1@86$*_z2&i15tg63zkoy0d0_a2jud-5id*a+-0*xm38fn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'courses',
    'organization',
    'operation',
    'xadmin',
    'crispy_forms',
    # 第三方验证码,
    'captcha',
    #分页
    'pure_pagination',
    # 富文本编辑器
    'ckeditor',
    # 文件上传功能在ckeditor_uploaderzhong
    'ckeditor_uploader',
]

# 自定用户模型
AUTH_USER_MODEL = 'users.User'

# 自定用户认证后端
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
    )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pymx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 添加文件处理器, 在模板中使用{{ MEDIA_URL }}
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'pymx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pymx',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# 用于开发环境静态文件处理
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

# DEBUG = False时, 设置STATIC_ROOT
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# 邮箱
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'taomiantm@sina.com'
EMAIL_HOST_PASSWORD = 'xxxxxx'
EMAIL_USE_TLS = False
EMAIL_FROM = 'taomiantm@sina.com'

# 服务器上传文件保存位置
# 简单理解:MEDIA_URL是浏览器通过url访问的url, MEDIA_ROOT是文件在服务器上的存放位置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ckeditor_uploader文件上传保存位置, 在media目录下
CKEDITOR_UPLOAD_PATH = 'upload/'


# 分页设置
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,

    # 'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}