# coding=utf-8
from south.management.commands import migrate
from django_sae.conf.settings import patch_sae_restful_mysql


class Command(migrate.Command):
    def handle(self, *args, **kwargs):
        patch_sae_restful_mysql()
        super(Command, self).handle(*args, **kwargs)
