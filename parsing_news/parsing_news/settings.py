import os

import raven

from utils.tools import create_directory

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'z++(zqx-7u1i*1*q_j8b(_k&xq-k8h5lph5_3vv!&zhce+h*a%'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'utils',
    'django_extensions',
    'django_celery_beat',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'parsing_news.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'parsing_news.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

CELERY_BROKER = 'redis://localhost:6379'

FILE_LOGGER = '/tmp/django_telegram/logs/debug.log'
FILE_HTTP_CLIENT_LOGGER = '/tmp/django_telegram/logs/http_client.log'
create_directory(FILE_LOGGER); create_directory(FILE_HTTP_CLIENT_LOGGER)

# CELERYD_HIJACK_ROOT_LOGGER = False  # TODO True
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose_with_extra': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d '
                      '%(extra)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': FILE_LOGGER,
            'formatter': 'verbose'
        },
        'file_http_client': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': FILE_HTTP_CLIENT_LOGGER,
            'formatter': 'verbose_with_extra'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'sentry': {
            'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
    },
    'loggers': {
        'tasks': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'HTTPClient': {
            'handlers': ['console', 'file_http_client'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'celery': {
            'handlers': ['sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

RAVEN_CONFIG = {
    'dsn': '',  # TODO put in secret file
}
