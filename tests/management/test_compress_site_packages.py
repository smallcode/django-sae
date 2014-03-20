# coding=utf-8
import os
from django_sae.management.commands import compress_site_packages
from .base import CommandTestBase


class CompressSitePackagesTest(CommandTestBase):
    def setUp(self):
        super(CompressSitePackagesTest, self).setUp()
        self.command = compress_site_packages.Command()

    def assertCompressed(self, command_output):
        self.assertIn("compressed success", command_output)
        zip_name = command_output.split(':')[-1]
        self.assertTrue(os.path.exists(zip_name))
        os.remove(zip_name)

    def test_command(self):
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