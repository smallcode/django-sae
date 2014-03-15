# coding=utf-8
from .environ import patch_http_host
from .modules import patch_pylibmc


def patch_local():
    patch_pylibmc()
    patch_http_host()