# coding=utf-8
"""Django settings for tests."""

import os
from django_sae.conf.settings import IN_SAE, STATIC_URL, TIME_ZONE, USE_TZ, LANGUAGE_CODE, USE_I18N

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

IN_SAE = IN_SAE
STATIC_URL = STATIC_URL
TIME_ZONE = TIME_ZONE
USE_TZ = USE_TZ
LANGUAGE_CODE = LANGUAGE_CODE
USE_I18N = USE_I18N

# Quick-start development settings - unsuitable for production

SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django_sae.contrib.patches',
    'django_sae.contrib.tasks',
    'tests',
]

MEDIA_URL = '/media/'  # Avoids https://code.djangoproject.com/ticket/21451

MIDDLEWARE_CLASSES = [
]

ROOT_URLCONF = 'tests.urls'

# Cache and database

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

from django_sae.contrib.patches.local import patch_local

patch_local()