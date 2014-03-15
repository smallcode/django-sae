# coding=utf-8
from django.conf import settings

from django_sae.contrib.patches.settings import patch_caches


def patch_root_urlconf():
    from django.conf.urls import include, patterns, url
    from django.core.urlresolvers import clear_url_caches, reverse, NoReverseMatch
    from django.utils.importlib import import_module

    try:
        reverse('tasks:execute')
    except NoReverseMatch:
        urlconf_module = import_module(settings.ROOT_URLCONF)
        urlconf_module.urlpatterns = patterns('',
                                              url(r'^tasks/', include('django_sae.contrib.tasks.urls', 'tasks', 'tasks')),
        ) + urlconf_module.urlpatterns
        clear_url_caches()


def patch_all():
    patch_root_urlconf()
    patch_caches()
