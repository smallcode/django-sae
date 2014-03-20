# coding=utf-8
from south.management.commands import syncdb
from django_sae.management.commands import patch_for_sae_restful_mysql, sae_migrate


class Command(syncdb.Command):
    def handle(self, *args, **kwargs):
        patch_for_sae_restful_mysql()
        # kwargs.setdefault('migrate', True) # 不起作用
        super(Command, self).handle(*args, **kwargs)
        sae_migrate.Command().execute()

