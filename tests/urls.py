# coding=utf-8
from django.conf.urls import patterns, url
from django_sae.contrib.tasks.tests.views import OperationViewMock

urlpatterns = patterns('',
                       url(r'^mock$', OperationViewMock.as_view()),
)