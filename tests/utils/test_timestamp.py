# coding=utf-8
import time

from django.test import SimpleTestCase as TestCase
from django.test.utils import override_settings

from django_sae.utils.timestamp import to_timestamp, to_datetime, make_timestamp


class TimestampTest(TestCase):
    def test_timestamp(self):
        ts = time.time()
        dt = to_datetime(ts)
        self.assertEqual(int(ts), to_timestamp(dt))

    @override_settings(USE_TZ=False)
    def test_timestamp_not_use_timezone(self):
        self.test_timestamp()

    @override_settings(USE_TZ=True, TIME_ZONE='Asia/Shanghai')
    def test_timestamp_use_timezone(self):
        self.test_timestamp()

    @override_settings(USE_TZ=False)
    def test_make_timestamp(self):
        self.assertEqual(make_timestamp(days=1) - make_timestamp(), 86400)
        self.assertEqual(make_timestamp(days=-1) - make_timestamp(), -86400)
