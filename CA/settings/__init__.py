# -*- coding: utf-8 -*-


from split_settings.tools import include
from os import environ


ENV = environ.get('DJANGO_ENV') or 'development'

base_settings = [
    'components/common.py',
    'components/logging.py',
    'components/secret_key.py',
    'environments/%s.py' % ENV,
]

include(*base_settings)
