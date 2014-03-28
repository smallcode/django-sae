# coding=utf-8
from django.conf import settings

ORDER_QUEUE_NAME = getattr(settings, 'ORDER_QUEUE_NAME', 'order')
PARALLEL_QUEUE_NAME = getattr(settings, 'PARALLEL_QUEUE_NAME', 'parallel')


def patch_root_urlconf():
    from django.conf.urls import include, patterns, url
    from django.core.urlresolvers import clear_url_caches, reverse, NoReverseMatch
    from django.utils.importlib import import_module

    try:
        reverse('tasks:execute')
    except NoReverseMatch:
        root = import_module(settings.ROOT_URLCONF)
        root.urlpatterns = patterns('', url(r'^tasks/', include('django_sae.contrib.tasks.urls', 'tasks',
                                                                'tasks')), ) + root.urlpatterns
        clear_url_caches()