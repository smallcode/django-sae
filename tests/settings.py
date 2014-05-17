# coding=utf-8
"""Django settings for tests."""

import os
from django_sae.conf.settings import IN_SAE

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = not IN_SAE

# Quick-start development settings - unsuitable for production

SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django_sae',
    'django_sae.contrib.tasks',
    'tests',
]

MIDDLEWARE_CLASSES = [
]

ROOT_URLCONF = 'tests.urls'

# database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# SOUTH_TESTS_MIGRATE=False