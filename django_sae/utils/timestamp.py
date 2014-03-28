# -*- coding:utf-8 -*-
import time
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone


def to_datetime(timestamp):
    dt = datetime.fromtimestamp(long(timestamp))
    if settings.USE_TZ:
        return dt.replace(tzinfo=timezone.get_current_timezone())
    return dt


def to_timestamp(dt):
    return int(time.mktime(dt.timetuple())) if isinstance(dt, datetime) else dt


def make_datetime(**kwargs):
    """
    已现在为起始的偏移日期，将来用整数，过去用负数，默认为现在
    kwargs: days, seconds, microseconds, milliseconds, minutes, hours, weeks
    如：make_datetime(days=-1)
    """
    return timezone.now() + timedelta(**kwargs)


def make_timestamp(**kwargs):
    """
    已现在为起始的偏移时间戳，将来用整数，过去用负数，默认为现在
    kwargs: days, seconds, microseconds, milliseconds, minutes, hours, weeks
    如：make_timestamp(days=-1)
    """
    return to_timestamp(make_datetime(**kwargs))