# coding=utf-8
from django.core.cache import cache
from django.test import SimpleTestCase as TestCase


class CacheTestBase(TestCase):
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