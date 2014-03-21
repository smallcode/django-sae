# coding=utf-8
import os
import sys
import sae.memcache
import sae._restful_mysql
from django.test import SimpleTestCase
from django_sae.conf import settings


class PatchesTestCase(SimpleTestCase):
    def test_patch_http_host(self):
        settings.patch_http_host()
        self.assertEqual(os.environ.get('HTTP_HOST'), 'localhost')

    def test_patch_disable_fetchurl(self):
        settings.patch_disable_fetchurl()
        self.assertEqual(os.environ.get('disable_fetchurl'), '1')

    def test_patch_pylibmc(self):
        settings.patch_pylibmc()
        self.assertEqual(sys.modules['pylibmc'], sae.memcache)

    def test_patch_sae_restful_mysql(self):
        settings.patch_sae_restful_mysql()
        self.assertEqual(sys.modules['MySQLdb'], sae._restful_mysql)

    def test_get_database(self):
        name = 'name'
        user = 'user'
        password = 'password'
        database = settings.get_database(name, user, password)
        self.assertEqual(database, {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': name,
                'USER': user,
                'PASSWORD': password,
                'HOST': settings.MYSQL_HOST,
                'PORT': settings.MYSQL_PORT,
                'OPTIONS': {'init_command': "SET storage_engine=MYISAM;"},
            }
        })