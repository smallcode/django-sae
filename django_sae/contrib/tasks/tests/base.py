# coding=utf-8
from django.test import SimpleTestCase as TestCase


class CronViewTestMixin(TestCase):
    def assertResult(self, r, count):
        self.assertEqual(200, r.status_code)
        self.assertEqual('added %s tasks' % count, r.content)