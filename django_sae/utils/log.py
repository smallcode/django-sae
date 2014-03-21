# coding=utf-8
import logging
from django.conf import settings
from django_sae.conf import settings as sae_settings


class RequireInSAE(logging.Filter):
    def filter(self, record):
        return getattr(settings, 'IN_SAE', sae_settings.IN_SAE)


class RequireNotInSAE(logging.Filter):
    def filter(self, record):
        return not getattr(settings, 'IN_SAE', sae_settings.IN_SAE)