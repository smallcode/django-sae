# coding=utf-8
from django.test import SimpleTestCase as TestCase
from django.test.utils import override_settings
from django.core.cache import cache


@override_settings(CACHES={
    'default': {
        'BACKEND': 'zidong.cache.backends.SaePyLibMCCache',
    }
})
class CacheTest(TestCase):
    def test_cache(self):
        key = 'my_key'
        value = 'hello, world!'
        cache.set(key, value, 3)
        self.assertEqual(cache.get(key), value)