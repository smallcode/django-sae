# coding=utf-8
from django.db.utils import DEFAULT_DB_ALIAS
from south.management.commands import syncdb
from django_sae.management.commands import patch_for_sae_restful_mysql, sae_migrate


class Command(syncdb.Command):
    def handle(self, *args, **kwargs):
        patch_for_sae_restful_mysql()
        # kwargs.setdefault('migrate', True)  # 不起作用
        # 设置DEFAULT_DB_ALIAS，避免测试时抛出异常：ConnectionDoesNotExist: The connection None doesn't exist
        kwargs.setdefault('database', DEFAULT_DB_ALIAS)
        super(Command, self).handle(*args, **kwargs)
        sae_migrate.Command().execute()

