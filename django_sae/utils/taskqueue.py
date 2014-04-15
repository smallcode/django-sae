# coding=utf-8
from sae.taskqueue import TaskQueue
from django.utils.six import string_types

CachedQueue = {}


def get_queue(queue_name):
    """ 获取队列
    """
    if queue_name not in CachedQueue:
        CachedQueue[queue_name] = TaskQueue(queue_name)
    return CachedQueue[queue_name]


def get_queue_size(queue_names):
    """ 获取队列中尚未执行的任务数
    """
    if isinstance(queue_names, string_types):
        names = [queue_names]
    else:
        names = list(iter(queue_names))
    return sum([get_queue(name).size() for name in names])