# coding=utf-8
from django.test import SimpleTestCase
from django_sae.utils.counts import count_length, count_pages


class CountsTest(SimpleTestCase):
    def test_count_pages(self):
        self.assertEqual(count_pages(10, 100), 10)
        self.assertEqual(count_pages(10, 99), 10)

    def test_count_length(self):
        self.assertEqual(count_length(u'中文'), 2)
        self.assertEqual(count_length(u'en'), 1)
        self.assertEqual(count_length(u'eng'), 2)
        self.assertEqual(count_length(u'中文en'), 3)
        self.assertEqual(count_length(u'中文eng'), 4)