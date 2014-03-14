# coding=utf-8

from django.core.cache.backends.memcached import BaseMemcachedCache, local


class SaePyLibMCCache(BaseMemcachedCache):
    """
    see: http://sae.sina.com.cn/?m=devcenter&catId=291#anchor_6c1bc2dacfd850c36fc3db0ec84e9ab3
         http://sae.sina.com.cn/?m=devcenter&catId=292#anchor_7267dff3baebb5655c19095bce390a7a
    """

    def __init__(self, server, params):
        import pylibmc

        self._local = local()
        #pylibmc.NotFound需更改为None,否则在本地会出现错误，模拟的sae.memcache中没有NotFound属性
        super(SaePyLibMCCache, self).__init__(server, params, library=pylibmc, value_not_found_exception=None)

    @property
    def _cache(self):
        client = getattr(self._local, 'client', None)
        if client:
            return client

        client = self._lib.Client()  # Client不需要传入参数
        if self._options:
            client.behaviors = self._options

        self._local.client = client

        return client
