# coding=utf-8
import os
import sys
import sae.memcache
import sae._restful_mysql
from django.test import SimpleTestCase
from django_sae.conf import settings


class PatchesTestCase(SimpleTestCase):
    def test_patch_disable_fetchurl(self):
        settings.patch_disable_fetchurl()
        self.assertEqual(os.environ.get('disable_fetchurl'), '1')

    def test_patch_task_queue(self):
        settings.patch_task_queue()
        self.assertEqual(os.environ.get('HTTP_HOST'), 'localhost:8080')

    def test_patch_memcache(self):
        settings.patch_memcache()
        self.assertEqual(sys.modules['pylibmc'], sae.memcache)

    def test_patch_kvdb(self):
        file_path = 'tests/kvdb'
        settings.patch_kvdb(file_path)
        self.assertEqual(os.environ['sae.kvdb.file'], os.path.abspath(file_path))

    def test_patch_storage(self):
        file_path = 'tests/storage'
        settings.patch_storage(file_path)
        self.assertEqual(os.environ['sae.storage.path'], os.path.abspath(file_path))

    def test_patch_app_info(self):
        name = 'django_sae'
        settings.patch_app_info(name)
        self.assertEqual(os.environ.get('APP_NAME'), name)
        self.assertEqual(os.environ.get('APP_VERSION'), '1')

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