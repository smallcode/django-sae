# coding=utf-8
import os

from django.test import SimpleTestCase

from django_sae.conf.patches import environ


class EnvironTestCase(SimpleTestCase):
    def test_patch_http_host(self):
        environ.patch_http_host()
        self.assertEqual(os.environ.get('HTTP_HOST'), 'localhost')

    def test_patch_disable_fetchurl(self):
        environ.patch_disable_fetchurl()
        self.assertEqual(os.environ.get('disable_fetchurl'), '1')

