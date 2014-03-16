# coding=utf-8
from cStringIO import StringIO
import os

from django.core.management import CommandError
from django.test import TestCase
from django.test.utils import override_settings

from django_sae.management.commands import updatepackages


class UpdatePackagesTestCase(TestCase):
    def setUp(self):
        self.stdout = StringIO()
        self.stderr = StringIO()

    def tearDown(self):
        self.stdout.close()
        self.stderr.close()

    @override_settings(PACKAGES_DIR='tests')
    def test_command(self):
        command = updatepackages.Command()
        zip_name = 'site-packages.zip'
        command.execute(zip_name=zip_name, stdout=self.stdout)
        command_output = self.stdout.getvalue().strip()
        self.assertEqual(command_output, "update and compress to file: %s success" % zip_name)
        self.assertTrue(os.path.exists(zip_name))
        os.remove(zip_name)

    @override_settings(PACKAGES_DIR=None)
    def test_command_without_packages_dir(self):
        command = updatepackages.Command()
        with self.assertRaises(CommandError):
            command.execute(stdout=self.stdout, stderr=self.stderr)