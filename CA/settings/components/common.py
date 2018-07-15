# -*- coding: utf-8 -*-
 
 
import os
from django.core.urlresolvers import reverse_lazy
 
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 
ALLOWED_HOSTS = ['127.0.0.1', 'admin.kase.kz', 'dashboard.kase.kz']
 
DEFAULT_CHARSET = 'utf-8'
 
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'django_select2',  # "django-select2" application
    'modeltranslation',  # "django-modeltranslation" application
    'reversion',  # django-reversion application
    'slider',  # "slider" application
    'static_pages',  # "static_pages" application
    'users',  # "users" application
    'el_pagination',  # django-el-pagination application
    'documents',  # 'documents' application
    'documents.templatetags',  # custom tags in 'documents' application
    'video',  # "video" application
    'indicators',  # "indicators" application
    'events',  # "events" application
    'faq',  # "faq" application
]

# Нужен для использования кастомных файлов (например: custom_clearable_file_input.html) в форме
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
 
ROOT_URLCONF = 'CA.urls'
 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
 
WSGI_APPLICATION = 'CA.wsgi.application'
 
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
 
LANGUAGE_CODE = 'ru'
 
LANGUAGES = (
    ('ru', 'Русский'),
    ('en', 'Английский'),
    ('kz', 'Казахский'),
)
 
# START: Model Translation Settings
MODELTRANSLATION_LANGUAGES = ('ru', 'en', 'kz')
 
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
# END: Model Translation Settings
 
TIME_ZONE = 'UTC'
 
USE_I18N = True
 
USE_L10N = True
 
USE_TZ = True
 
# START: Static and Media files settings
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
 
STATIC_URL = '/static/'
 
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
 
MEDIA_URL = '/media/'
 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
# END: Static and Media files settings

LOGIN_REDIRECT_URL = reverse_lazy('dashboard')
LOGIN_URL = reverse_lazy('administration_login')
