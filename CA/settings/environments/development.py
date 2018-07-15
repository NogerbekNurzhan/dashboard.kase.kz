# -*- coding: utf-8 -*-


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': '...',
        'USER': '...',
        'PASSWORD': '...',
    }
}

DOCUMENT_FILE_STORAGE = '/Applications/Projects/web/file.kase.kz/private/'

EVENT_IMAGE_STORAGE = '/Applications/Projects/web/file.kase.kz/public/'
