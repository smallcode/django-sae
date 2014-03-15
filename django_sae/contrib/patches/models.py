# coding=utf-8
from django_sae.conf import settings as sae_settings
from django_sae.contrib.patches.environ import patch_http_host
from django_sae.contrib.patches.modules import patch_pylibmc
from django_sae.contrib.patches.settings import patch_caches, patch_databases


patch_caches()
if sae_settings.IN_SAE:
    patch_databases()
else:
    patch_pylibmc()
    patch_http_host()