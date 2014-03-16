# coding=utf-8
import sys
import sae.memcache
from django.test import SimpleTestCase
from django_sae.contrib.patches import modules


class ModulesTestCase(SimpleTestCase):
    def test_patch_pylibmc(self):
        modules.patch_pylibmc()
        self.assertEqual(sys.modules['pylibmc'], sae.memcache)

