# coding=utf-8
import os
from django.test import SimpleTestCase
from django.test.utils import override_settings
from django.conf import settings
from django_sae.conf import settings as sae_settings
from django_sae.contrib.patches import settings as p_settings


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    },
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
)
class SettingsTestCase(SimpleTestCase):
    def test_patch_caches(self):
        p_settings.patch_caches()
        self.assertEqual(settings.CACHES, sae_settings.CACHES)

    def test_patch_databases(self):
        p_settings.patch_databases()
        self.assertEqual(settings.DATABASES, sae_settings.DATABASES)

    def assertDatabase(self, db):
        self.assertEqual(db['NAME'], 'db')
        self.assertEqual(db['USER'], 'user')
        self.assertEqual(db['PASSWORD'], 'pass')

    @override_settings(
        MYSQL_DB='db',
        MYSQL_USER='user',
        MYSQL_PASS='pass',
    )
    def test_patch_custom_databases(self):
        p_settings.patch_databases()
        self.assertEqual(settings.DATABASES, sae_settings.DATABASES)
        self.assertDatabase(settings.DATABASES['default'])
        self.assertDatabase(settings.DATABASES['slave'])

    def test_patch_databases_routers(self):
        p_settings.patch_databases_routers()
        self.assertEqual(settings.DATABASE_ROUTERS, sae_settings.DATABASE_ROUTERS)

    @override_settings(
        IN_SAE=True,
        DISABLE_FETCHURL=True,
    )
    def test_patch_all(self):
        p_settings.patch_all()
        self.assertEqual(settings.CACHES, sae_settings.CACHES)
        self.assertEqual(settings.DATABASES, sae_settings.DATABASES)
        self.assertEqual(settings.DATABASE_ROUTERS, sae_settings.DATABASE_ROUTERS)
        self.assertEqual(os.environ.get('disable_fetchurl'), '1')

    def test_patch_syncdb(self):
        name = 'name'
        user = 'user'
        password = 'password'
        p_settings.patch_syncdb(name, user, password)
        self.assertEqual(settings.DATABASES, {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': name,
                'USER': user,
                'PASSWORD': password,
                'HOST': 'w.rdc.sae.sina.com.cn',
                'PORT': '3307',
                'OPTIONS': {'init_command': "SET storage_engine=MYISAM;"},
            }})
        self.assertEqual(settings.DATABASE_ROUTERS, [])
