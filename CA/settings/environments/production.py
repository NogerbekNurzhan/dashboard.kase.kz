# -*- coding: utf-8 -*-


DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': '...',
        'USER': '...',
        'PASSWORD': '...',
        'OPTIONS': {
            'threaded': True,
        }
    }
}

DOCUMENT_FILE_STORAGE = '/srv/www/files.kase.kz/private/'

EVENT_IMAGE_STORAGE = '/srv/www/files.kase.kz/public/'
