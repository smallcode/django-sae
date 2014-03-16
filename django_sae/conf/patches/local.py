# coding=utf-8
from django_sae.conf.patches.environ import patch_http_host
from django_sae.conf.patches.modules import patch_pylibmc


def patch_local():
    patch_pylibmc()
    patch_http_host()