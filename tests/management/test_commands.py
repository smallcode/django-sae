# coding=utf-8
from distutils.sysconfig import get_python_lib
import os
import shutil
from cStringIO import StringIO
from django.conf import settings
from django.core.management import CommandError
from django.test import SimpleTestCase
from django.test.utils import override_settings
import pip
from pip.commands import UninstallCommand
from django_sae.management.commands import (compress_site_packages, upgrade_requirements, patch_for_sae_restful_mysql,
                                            sae_migrate, sae_schemamigration, sae_syncdb)

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


class CompressSitePackagesTest(CommandTestBase):
    def setUp(self):
        super(CompressSitePackagesTest, self).setUp()
        self.command = compress_site_packages.Command()

    def assertCompressed(self, command_output):
        self.assertIn("compressed success", command_output)
        zip_name = command_output.split(':')[-1]
        self.assertTrue(os.path.exists(zip_name))
        os.remove(zip_name)

    def test_compress_site_packages(self):
        command_output = self.execute(self.command, path='tests', clean_pyc=True)
        self.assertCompressed(command_output)

    def test_compress_site_packages_without_clean_pyc(self):
        command_output = self.execute(self.command, path='tests', clean_pyc=False)
        self.assertCompressed(command_output)

    def test_replace_site_packages(self):
        origin_zip_name = 'site-packages123.zip'
        zip_name = 'site-packages456.zip'
        path = os.path.join('tests', 'index.wsgi')
        self.command.replace_site_packages(path, zip_name)
        with open(path) as wsgi_file:
            self.assertIn("sys.path.insert(0, os.path.join(root, '%s'))" % zip_name, wsgi_file.read())
        self.command.replace_site_packages(path, origin_zip_name)  # 复原

    def test_check_file(self):
        self.assertFalse(self.command.check_file('', 'foo.pth'))
        self.assertTrue(self.command.check_file('', 'foo.py'))

    def test_check_root(self):
        for module in self.command.filter_modules:
            self.assertFalse(self.command.check_root(module))
        self.assertFalse(self.command.check_root('test.egg-info'))
        self.assertTrue(self.command.check_root('foo'))


@override_settings(INSTALLED_APPS=[
    APP,
])
class CommandsTestCase(CommandTestBase):
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
        shutil.rmtree(path)

    def test_sae_syncdb(self):
        command = sae_syncdb.Command()
        with self.assertRaises(Exception):
            self.execute(command)
        self.assertPatched()

    def get_package_path(self, package):
        return os.path.join(get_python_lib(), package)

    def uninstall(self, package):
        cmd_name, args = pip.parseopts(['uninstall', '--yes', package])
        UninstallCommand().main(args)
        self.assertFalse(os.path.exists(self.get_package_path(package)))

    def test_upgrade_requirements(self):
        package = 'requests'
        command = upgrade_requirements.Command()
        self.execute(command, requirements=['tests/requirements.txt'])
        self.assertTrue(os.path.exists(self.get_package_path(package)))
        self.uninstall(package)


