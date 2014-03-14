# coding=utf-8
from django_sae.cache import models


class ModelMock(models.Model):
    KEYS = ('uid',)
    VALUES = ('name',)

    def __init__(self, uid, name, expires_in=None):
        super(ModelMock, self).__init__(expires_in)
        self.uid = uid
        self.name = name


class ManagerModelMock(object):
    def __init__(self, pk):
        self.pk = pk