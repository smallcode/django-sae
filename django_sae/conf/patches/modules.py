# coding=utf-8
import sys


def patch_pylibmc():
    """ Add dummy pylibmc module,用于本地测试
    """
    import sae.memcache

    sys.modules['pylibmc'] = sae.memcache