# coding=utf-8
import os
import shutil
from django_sae.management.commands import sae_syncdb
from south.management.commands import schemamigration
from .base import CommandTestBase


class SaeSyncdbTestCase(CommandTestBase):
    def delete_migrations(self, app):
        path = os.path.join(app, 'migrations')
        if os.path.exists(path):
            shutil.rmtree(path)

    def test_command(self):
        app = 'tests'
        schemamigration.Command().execute(app=app, initial=True)
        command = sae_syncdb.Command()
        self.execute(command, verbosity=1)
        self.delete_migrations(app)


