# coding=utf-8
from django.core.management.commands import migrate
from django.db.utils import DEFAULT_DB_ALIAS
from django_sae.conf.settings import patch_sae_restful_mysql


class Command(migrate.Command):
    def handle(self, *args, **kwargs):
        patch_sae_restful_mysql()
        kwargs.setdefault('database', DEFAULT_DB_ALIAS)
        super(Command, self).handle(*args, **kwargs)
