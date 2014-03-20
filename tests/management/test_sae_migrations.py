# coding=utf-8
import os
import shutil
from django_sae.management.commands import sae_migrate, sae_schemamigration
from .base import CommandTestBase


class CommandsTestCase(CommandTestBase):
    def test_sae_migrate(self):
        command = sae_migrate.Command()
        self.execute(command)

    def test_sae_schema_migration(self):
        app = 'tests'
        command = sae_schemamigration.Command()
        self.execute(command, app, initial=True)
        path = os.path.join(app, 'migrations')
        self.assertTrue(os.path.exists(path))
        shutil.rmtree(path)


