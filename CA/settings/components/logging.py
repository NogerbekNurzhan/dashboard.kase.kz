# -*- coding: utf-8 -*-


from CA.formatter import ColoredFormatter


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': ColoredFormatter,
            'format': 'Time: [%(asctime)s] | LevelName: %(levelname)s | Module: %(module)s | Process: %(process)d | Thread: %(thread)d | Message: %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
        'simple': {
            'format': '[%(asctime)s] | %(levelname)s | %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logging/debug.log',
            'maxBytes': 1024*1024*5,
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'handlers': ['console', 'logfile'],
        },
    },
}