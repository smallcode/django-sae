# coding=utf-8
import os
import shutil
from django.test.utils import override_settings
from django_sae.management.commands import sae_migrate, sae_schemamigration
from .base import CommandTestBase, MYSQL_DB, MYSQL_USER, MYSQL_PASS


@override_settings(
    MYSQL_DB=MYSQL_DB,
    MYSQL_USER=MYSQL_USER,
    MYSQL_PASS=MYSQL_PASS,
)
class CommandsTestCase(CommandTestBase):
    def test_sae_migrate(self):
        command = sae_migrate.Command()
        self.execute(command)
        self.assertPatched()

    def test_sae_schema_migration(self):
        app = 'tests'
        command = sae_schemamigration.Command()
        self.execute(command, app, initial=True)
        self.assertPatched()
        path = os.path.join(app, 'migrations')
        self.assertTrue(os.path.exists(path))
        shutil.rmtree(path)


