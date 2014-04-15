# coding=utf-8
from django.test import SimpleTestCase as TestCase
from django.core.cache import cache

from django_sae.contrib.tasks.operations import OperationBase, TaskOperationMixin
from django_sae.contrib.tasks.tests.operations import OperationMock


class OperationTest(TestCase):
    def test_execute_when_raise_error(self):
        self.assertRaises(NotImplementedError, OperationBase().execute)

    def test_execute(self):
        r = OperationMock().execute()
        self.assertEqual(r, 'foo')

    def test_data(self):
        self.data = dict(foo='bar')
        self.operation = OperationMock(**self.data)
        self.assertEqual(self.operation.data, self.data)


class TaskOperationTest(TestCase):
    def setUp(self):
        self.operation = TaskOperationMixin()

    def tearDown(self):
        cache.clear()

    def test_save_to_mc(self):
        key = self.operation.get_key()
        self.assertIn(self.operation.__class__.__name__, key)
        self.assertIn(self.operation.__module__.split('.')[0], key)
        self.operation.save_to_mc(key)
        self.assertIsNotNone(cache.get(key))

    def test_execute_by_queue(self):
        r = self.operation.execute_by_queue('test')
        self.assertTrue(r)

    def test_execute_by_order(self):
        r = self.operation.execute_by_order()
        self.assertTrue(r)

    def test_execute_by_parallel(self):
        r = self.operation.execute_by_parallel()
        self.assertTrue(r)

    def test_get_total_page(self):
        self.assertEqual(self.operation.get_total_page(10, 100), 10)
        self.assertEqual(self.operation.get_total_page(10, 99), 10)
