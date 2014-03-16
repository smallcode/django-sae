# coding=utf-8
import os
import sys
import sae.memcache

from django.test import SimpleTestCase
from django_sae.contrib.patches import local


class LocalTestCase(SimpleTestCase):
    def test_patch_local(self):
        local.patch_local()
        self.assertEqual(os.environ.get('HTTP_HOST'), 'localhost')
        self.assertEqual(sys.modules['pylibmc'], sae.memcache)

