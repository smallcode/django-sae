# coding=utf-8
from django.core.management import CommandError
from django.test.utils import override_settings
from django_sae.management.commands import patch_for_sae_restful_mysql
from .base import PatchTestBase, MYSQL_DB, MYSQL_USER, MYSQL_PASS


@override_settings(
    MYSQL_DB=MYSQL_DB,
    MYSQL_USER=MYSQL_USER,
    MYSQL_PASS=MYSQL_PASS,
)
class PatchesTestCase(PatchTestBase):
    def test_patch_for_sae_restful_mysql(self):
        patch_for_sae_restful_mysql()
        self.assertPatched()

    @override_settings(
        MYSQL_USER=None,
        MYSQL_PASS=None,
    )
    def test_patch_for_sae_restful_mysql_without_settings(self):
        with self.assertRaises(CommandError):
            patch_for_sae_restful_mysql()