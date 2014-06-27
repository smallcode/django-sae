# coding=utf-8
from django.test import TestCase
from django_sae.db.routers import MasterSlaveRouter


class MasterSlaveRouterTest(TestCase):
    def setUp(self):
        self.router = MasterSlaveRouter()

    def test_db_for_read(self):
        self.assertEqual(self.router.db_for_read(None), 'slave')

    def test_db_for_write(self):
        self.assertTrue(self.router.db_for_write(None), 'master')

    def test_allow_syncdb(self):
        self.assertTrue(self.router.allow_syncdb(None, None))

    def test_allow_relation(self):
        self.assertTrue(self.router.allow_relation(None, None))
