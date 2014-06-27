# coding=utf-8
from django.db import models
from django_sae.db.models import AutoIdEntity


class User(AutoIdEntity):
    name = models.CharField(max_length=75)
