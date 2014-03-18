# coding=utf-8
"""Django settings for tests."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production

SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django_sae.contrib.tasks',
    'tests',
]

MEDIA_URL = '/media/'  # Avoids https://code.djangoproject.com/ticket/21451

MIDDLEWARE_CLASSES = [
]

ROOT_URLCONF = 'tests.urls'

# database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

from django_sae.conf.patches.local import patch_local

patch_local()