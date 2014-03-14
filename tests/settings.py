# coding=utf-8
"""Django settings for tests."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production

SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django_sae',
    'tests',
]

MEDIA_URL = '/media/'   # Avoids https://code.djangoproject.com/ticket/21451

MIDDLEWARE_CLASSES = [
]

ROOT_URLCONF = 'tests.urls'


# Cache and database

CACHES = {
    'default': {
        'BACKEND': 'django_sae.cache.backends.SaePyLibMCCache',
        'TIMEOUT': 86400,
        'VERSION': 1,
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

import sys
import sae.memcache

# Add dummy pylibmc module,本地测试用
sys.modules['pylibmc'] = sae.memcache


# 设置本地TaskQueue测试时需要的参数，否则test时client会出错
os.environ.setdefault('HTTP_HOST', 'localhost:8080')