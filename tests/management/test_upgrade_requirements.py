# coding=utf-8
import os
import pip
from pip.commands import UninstallCommand
from distutils.sysconfig import get_python_lib
from django_sae.management.commands import upgrade_requirements
from .base import CommandTestBase


class UpgradeRequirementsTestCase(CommandTestBase):
    def is_exists(self, package):
        return os.path.exists(os.path.join(get_python_lib(), package)) or os.path.exists(
            os.path.join(get_python_lib(), '%s.py' % package))

    def uninstall(self, package):
        cmd_name, args = pip.parseopts(['uninstall', '--yes', package])
        UninstallCommand().main(args)
        self.assertFalse(self.is_exists(package))

    def test_command(self):
        package = 'requests'
        command = upgrade_requirements.Command()
        self.execute(command, requirements=['tests/requirements.txt'])
        self.assertTrue(self.is_exists(package))
        self.uninstall(package)