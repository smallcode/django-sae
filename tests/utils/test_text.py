# coding=utf-8
from django.test import SimpleTestCase
from django_sae.utils.text import any_in


class TextTest(SimpleTestCase):
    def test_any_in(self):
        self.assertTrue(any_in([u'测试'], u'这是个测试语句'))
        self.assertFalse(any_in([u'不包含'], u'这是个测试语句'))