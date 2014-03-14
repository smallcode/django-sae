# coding=utf-8
from django.conf.urls import patterns, url, include
from django_sae.contrib.tasks.tests.views import OperationViewMock


urlpatterns = patterns('',
                       url(r'^tasks/', include('django_sae.contrib.tasks.urls')),
                       url(r'^mock$', OperationViewMock.as_view()),
)