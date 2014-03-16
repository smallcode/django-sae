# coding=utf-8
from django.conf import settings
from django_sae.conf import settings as sae_settings
from .environ import patch_disable_fetchurl


def is_in_sae():
    return getattr(settings, 'IN_SAE', sae_settings.IN_SAE)


def is_disable_fetchurl():
    return getattr(settings, 'DISABLE_FETCHURL', False)


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
    custom = {
        'NAME': getattr(settings, 'MYSQL_DB', sae_settings.MYSQL_DB),
        'USER': getattr(settings, 'MYSQL_USER', sae_settings.MYSQL_USER),
        'PASSWORD': getattr(settings, 'MYSQL_PASS', sae_settings.MYSQL_PASS),
    }
    sae_settings.DATABASES['default'].update(custom)
    sae_settings.DATABASES['slave'].update(custom)
    set_setting('DATABASES', sae_settings.DATABASES)


def patch_databases_routers():
    prepend_to_setting('DATABASE_ROUTERS', sae_settings.DATABASE_ROUTERS[0])


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
    if is_in_sae():
        patch_databases()
        patch_databases_routers()
        if is_disable_fetchurl():
            patch_disable_fetchurl()