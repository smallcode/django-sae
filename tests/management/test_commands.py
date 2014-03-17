# coding=utf-8
import os
from django.conf import settings
from django.core.management import CommandError
from django.test import SimpleTestCase
from cStringIO import StringIO
from django.test.utils import override_settings
from django_sae.management.commands import patch_for_sae_restful_mysql, sae_migrate, sae_schemamigration, sae_syncdb, \
    compress_site_packages

MYSQL_USER = 'user'
MYSQL_PASS = 'pass'
APP = 'django_sae.contrib.tasks'


@override_settings(
    MYSQL_USER=MYSQL_USER,
    MYSQL_PASS=MYSQL_PASS,
)
class PatchTestBase(SimpleTestCase):
    def assertPatched(self):
        self.assertEqual(settings.DATABASES, {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'app_tests',
                'USER': MYSQL_USER,
                'PASSWORD': MYSQL_PASS,
                'HOST': 'w.rdc.sae.sina.com.cn',
                'PORT': '3307',
                'OPTIONS': {'init_command': "SET storage_engine=MYISAM;"},
            }})
        self.assertEqual(settings.DATABASE_ROUTERS, [])


class CommandTestBase(PatchTestBase):
    def setUp(self):
        self.stdout = StringIO()
        self.stderr = StringIO()

    def tearDown(self):
        self.stdout.close()
        self.stderr.close()

    def execute(self, command, *args, **options):
        options.setdefault('stdout', self.stdout)
        options.setdefault('stderr', self.stderr)
        command.execute(*args, **options)
        return self.stdout.getvalue().strip()


class PatchesTestCase(PatchTestBase):
    def test_patch_for_sae_restful_mysql(self):
        patch_for_sae_restful_mysql()
        self.assertPatched()

    @override_settings(
        MYSQL_USER=None,
        MYSQL_PASS=None,
    )
    def test_patch_for_sae_restful_mysql_without_settings(self):
        with self.assertRaises(CommandError):
            patch_for_sae_restful_mysql()


@override_settings(INSTALLED_APPS=[
    APP,
])
class CommandsTestCase(CommandTestBase):
    @override_settings(PACKAGES_DIR='tests')
    def test_command(self):
        command = compress_site_packages.Command()
        command_output = self.execute(command)
        self.assertIn("compressed success", command_output)
        zip_name = command_output.split(':')[-1]
        self.assertTrue(os.path.exists(zip_name))
        os.remove(zip_name)

    @override_settings(PACKAGES_DIR=None)
    def test_command_without_packages_dir(self):
        command = compress_site_packages.Command()
        with self.assertRaises(CommandError):
            command.execute(stdout=self.stdout, stderr=self.stderr)

    def test_sae_migrate(self):
        command = sae_migrate.Command()
        self.execute(command)
        self.assertPatched()

    def test_sae_schema_migration(self):
        command = sae_schemamigration.Command()
        self.execute(command, APP, empty=True)
        self.assertPatched()
        path = os.path.join(*(APP.split('.') + ['migrations']))
        self.assertTrue(os.path.exists(path))
        # os.removedirs(path)

    def test_sae_syncdb(self):
        command = sae_syncdb.Command()
        with self.assertRaises(Exception):
            self.execute(command)
        self.assertPatched()