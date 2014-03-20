# coding=utf-8
from cStringIO import StringIO
from django.test import SimpleTestCase


class CommandTestBase(SimpleTestCase):
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