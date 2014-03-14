# coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^execute/(?P<key>.+)/$', 'django_sae.contrib.tasks.views.execute', name='execute'),
)