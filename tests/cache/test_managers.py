# coding=utf-8
from django_sae.cache.managers import Manager
from tests.cache.base import CacheTestBase
from tests.cache.models import ManagerModelMock


class ManagerMock(ManagerModelMock):
    manager = Manager()


class ManagerTest(CacheTestBase):
    def setUp(self):
        self.obj = ManagerMock(123)

    def test_get(self):
        self.assertEqual(self.obj.manager.instance, self.obj)

    def test_value_error(self):
        self.assertRaises(ValueError, lambda: ManagerMock(None).manager.instance)
        self.assertRaises(ValueError, lambda: ManagerMock.manager.func())