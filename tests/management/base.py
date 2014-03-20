# coding=utf-8
from cStringIO import StringIO
from django.conf import settings
from django.test import SimpleTestCase
from django.db.utils import DEFAULT_DB_ALIAS
from sae.const import MYSQL_HOST, MYSQL_PORT

MYSQL_DB = 'app_tests'
MYSQL_USER = 'user'
MYSQL_PASS = 'pass'


class PatchTestBase(SimpleTestCase):
    def assertPatched(self, name=MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASS, db_alias=DEFAULT_DB_ALIAS):
        db = settings.DATABASES[db_alias]
        self.assertEqual(db['ENGINE'], 'django.db.backends.mysql')
        self.assertEqual(db['NAME'], name)
        self.assertEqual(db['USER'], user)
        self.assertEqual(db['PASSWORD'], password)
        self.assertEqual(db['HOST'], MYSQL_HOST)
        self.assertEqual(db['PORT'], MYSQL_PORT)
        self.assertEqual(settings.DATABASE_ROUTERS, [])


class CommandTestBase(PatchTestBase):
    def setUp(self):
        self.maxDiff = None
        self.stdout = StringIO()
        self.stderr = StringIO()

    def tearDown(self):
        self.stdout.close()
        self.stderr.close()

    def execute(self, command, *args, **options):
        options.setdefault('stdout', self.stdout)
        options.setdefault('stderr', self.stderr)
        command.execute(*args, **options)
        return self.stdout.getvalue().strip()