# coding=utf-8
from django.test import SimpleTestCase
from django.test.utils import override_settings
from django.core.cache import cache


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django_sae.cache.backends.SaePyLibMCCache',
        }
    })
class CacheTestBase(SimpleTestCase):
    def tearDown(self):
        cache.clear()


class ModelTestBase(CacheTestBase):
    def assertCache(self, model):
        model.save()
        self.assertEqual(cache.get(model.key), model.value)

    def assertNotCache(self, model):
        model.save()
        self.assertIsNone(cache.get(model.key))

    def assertIsExpires(self, model):
        self.assertTrue(model.is_expires)

    def assertIsNotExpires(self, model):
        self.assertFalse(model.is_expires)