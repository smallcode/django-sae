# coding=utf-8
from django.conf import settings
from django_sae.conf import settings as sae_settings
from .environ import patch_disable_fetchurl
from .local import patch_local

DISABLE_FETCHURL = getattr(settings, 'DISABLE_FETCHURL', False)


def is_local_mem_cache():
    return settings.CACHES['default']['BACKEND'] == 'django.core.cache.backends.locmem.LocMemCache'


def set_setting(setting_name, value):
    setattr(settings, setting_name, value)


def prepend_to_setting(setting_name, value):
    """Insert value at the beginning of a list or tuple setting."""
    values = getattr(settings, setting_name)
    # Make a list [value] or tuple (value,)
    value = type(values)((value,))
    set_setting(setting_name, value + values)


def patch_caches():
    if not settings.CACHES or is_local_mem_cache():
        set_setting('CACHES', sae_settings.CACHES)


def patch_databases():
    set_setting('DATABASES', sae_settings.DATABASES)
    set_setting('DATABASE_ROUTERS', sae_settings.DATABASE_ROUTERS)


def patch_syncdb(name, user, password):
    set_setting('DATABASES', {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'HOST': 'w.rdc.sae.sina.com.cn',
            'PORT': '3307',
            'OPTIONS': {'init_command': "SET storage_engine=MYISAM;"},
        }})
    set_setting('DATABASE_ROUTERS', [])
    from sae._restful_mysql import monkey

    monkey.patch()


def patch_all():
    patch_caches()
    if sae_settings.IN_SAE:
        patch_databases()
        if DISABLE_FETCHURL:
            patch_disable_fetchurl()
    else:
        patch_local()