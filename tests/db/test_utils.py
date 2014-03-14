# coding=utf-8
from django.test import SimpleTestCase as TestCase
from django.db import connection

from django_sae.db.utils import print_sql, clear_sql


class UtilsTest(TestCase):
    def setUp(self):
        query_mock = {'time': 1, 'sql': 'sql mock'}
        connection.queries = [query_mock]

    def test_print_url(self):
        print_sql()

    def test_clear_sql(self):
        clear_sql()
        self.assertFalse(connection.queries)