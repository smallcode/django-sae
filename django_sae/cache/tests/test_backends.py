# coding=utf-8
from django_sae.cache.tests.base import CacheTestBase
from django.core.cache import cache


class CacheTest(CacheTestBase):
    def test_cache(self):
        key = 'my_key'
        value = 'hello, world!'
        cache.set(key, value, 3)
        self.assertEqual(cache.get(key), value)