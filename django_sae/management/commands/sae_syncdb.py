# coding=utf-8
from south.management.commands import syncdb
from django_sae.management.commands import patch_for_sae_restful_mysql


class Command(syncdb.Command):
    def handle(self, *args, **kwargs):
        patch_for_sae_restful_mysql()
        kwargs.setdefault('migrate', True)
        super(Command, self).handle(*args, **kwargs)
