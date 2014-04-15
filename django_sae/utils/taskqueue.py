# coding=utf-8
from sae.taskqueue import TaskQueue

CachedQueue = {}


def get_queue(queue_name):
    if queue_name not in CachedQueue:
        CachedQueue[queue_name] = TaskQueue(queue_name)
    return CachedQueue[queue_name]