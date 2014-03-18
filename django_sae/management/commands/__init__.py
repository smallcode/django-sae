# coding=utf-8
from django.conf import settings
from django.core.management.base import CommandError


def get_app_name():
    return settings.ROOT_URLCONF.split('.')[0]


def patch_for_sae_restful_mysql():
    host = getattr(settings, 'MYSQL_HOST', 'w.rdc.sae.sina.com.cn')
    port = getattr(settings, 'MYSQL_PORT', '3307')
    name = getattr(settings, 'MYSQL_DB', '_'.join(['app', get_app_name()]))
    user = getattr(settings, 'MYSQL_USER', None)
    password = getattr(settings, 'MYSQL_PASS', None)
    if name is None or user is None or password is None:
        raise CommandError('MYSQL_DB or MYSQL_USER or MYSQL_PASS is None, it should be set in settings')
    setattr(settings, 'DATABASES', {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
            'OPTIONS': {'init_command': "SET storage_engine=MYISAM;"},
        }})
    setattr(settings, 'DATABASE_ROUTERS', [])
    from sae._restful_mysql import monkey

    monkey.patch()