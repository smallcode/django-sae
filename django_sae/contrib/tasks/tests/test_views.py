# coding=utf-8
from django.test import SimpleTestCase as TestCase
from django.core.cache import cache

from django_sae.contrib.tasks.tests.operations import TaskOperationMock


class ViewsTest(TestCase):
    def setUp(self):
        self.operation = TaskOperationMock('foo')
        self.key = self.operation.get_key()
        self.uri = self.operation.get_execute_uri(self.key)

    def tearDown(self):
        cache.clear()

    def test_execute(self):
        self.operation.save_to_mc(self.key)
        response = self.client.get(self.uri)
        self.assertContains(response, 'success')
        self.assertIsNone(cache.get(self.key))

    def test_execute_not_exist_key(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(cache.get(self.key))
