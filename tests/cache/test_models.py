# coding=utf-8
import time

from tests.cache.base import ModelTestBase
from tests.cache.models import ModelMock


class ModelTest(ModelTestBase):
    def setUp(self):
        self.name = 'name'
        self.expires_in = 3
        self.uid = 123

    def test_save(self):
        model = ModelMock('123', self.name, self.expires_in)
        self.assertIsNotExpires(model)
        self.assertEqual(model.expires_in, model.expires_in)
        self.assertEqual(model.key, 'ModelMock_123')
        self.assertEqual(model.value['name'], 'name')
        self.assertGreater(model.value['expired_at'], time.time())
        self.assertCache(model)

    def test_delete(self):
        model = ModelMock('123', self.name, self.expires_in)
        model.save()
        model.delete()
        self.assertIsExpires(model)
        self.assertIsExpires(ModelMock('123', self.name))

    def test_check_cache(self):
        model = ModelMock(self.uid, self.name, self.expires_in)
        model.save()
        self.assertIsNotExpires(ModelMock(self.uid, self.name))

    def test_is_expires(self):
        model = ModelMock(self.uid, self.name, expires_in=-1)
        self.assertIsExpires(model)
        self.assertNotCache(model)

    def test_none_expires_in(self):
        model = ModelMock(self.uid, self.name, expires_in=None)
        self.assertIsExpires(model)
        self.assertNotCache(model)

    def test_key_error(self):
        model = ModelMock(None, self.name, self.expires_in)
        self.assertRaises(KeyError, lambda: model.save())

    def test_value_error(self):
        model = ModelMock(self.uid, None, self.expires_in)
        self.assertRaises(ValueError, lambda: model.save())





