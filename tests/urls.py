# coding=utf-8
from django.conf.urls import include, patterns, url

urlpatterns = patterns('',
                       url(r'^tasks/', include('django_sae.contrib.tasks.urls')),
)