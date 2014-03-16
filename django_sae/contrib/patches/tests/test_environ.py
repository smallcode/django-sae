# coding=utf-8
from django.test import SimpleTestCase
import os

from django_sae.contrib.patches import environ


class EnvironTestCase(SimpleTestCase):
    def test_patch_http_host(self):
        environ.patch_http_host()
        self.assertEqual(os.environ.get('HTTP_HOST'), 'localhost')

    def test_patch_disable_fetchurl(self):
        environ.patch_disable_fetchurl()
        self.assertEqual(os.environ.get('disable_fetchurl'), '1')

