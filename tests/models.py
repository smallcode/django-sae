# coding=utf-8
from django.db import models
from django_sae.db.models import AutoIdEntity


class Passport(AutoIdEntity):
    username = models.CharField(primary_key=True, max_length=75)
    password = models.CharField(max_length=128, blank=False)
    email = models.EmailField(blank=True)

    def __unicode__(self):
        return self.username