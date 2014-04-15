# coding=utf-8
import random
import time

from django.core.urlresolvers import reverse
from django.core.cache import cache
from django_sae.contrib.tasks.settings import ORDER_QUEUE_NAME, PARALLEL_QUEUE_NAME
from django_sae.utils.taskqueue import get_queue
from sae.taskqueue import Task


class OperationBase(object):
    def __init__(self, **kwargs):
        self.data = kwargs

    def pre_post(self):
        pass

    def post(self):
        raise NotImplementedError

    def save(self, response):
        pass

    def next(self, response):
        pass

    def execute(self):
        self.pre_post()
        response = self.post()
        if response is not None:
            self.save(response)
            self.next(response)
            return response


class TaskOperationMixin(object):
    QUEUE_NAME = PARALLEL_QUEUE_NAME

    @staticmethod
    def get_random_id(digits=8):
        return 'r%d' % (int(time.time()) + random.randint(0, pow(10, digits) - 1))

    def get_key_fields(self):
        return [self.get_random_id()]

    def get_key(self):
        fields = [self.__module__.split('.')[0], self.__class__.__name__]
        sub_fields = self.get_key_fields()
        if sub_fields:
            fields.extend(sub_fields)
        return '.'.join([str(field) for field in fields])

    def save_to_mc(self, key):
        cache.set(key, self)

    @staticmethod
    def get_execute_uri(key):
        return reverse('tasks:execute', kwargs={'key': key})

    def as_task(self, **kwargs):
        key = self.get_key()
        self.save_to_mc(key)
        return Task(self.get_execute_uri(key), **kwargs)

    def execute_by_queue(self, queue_name=QUEUE_NAME, **kwargs):
        task = self.as_task(**kwargs)
        queue = get_queue(queue_name)
        return queue.add(task)

    def execute_by_order(self, **kwargs):
        return self.execute_by_queue(ORDER_QUEUE_NAME, **kwargs)

    def execute_by_parallel(self, **kwargs):
        return self.execute_by_queue(PARALLEL_QUEUE_NAME, **kwargs)

    @staticmethod
    def get_total_page(page_length, total_number):
        quotient, remainder = divmod(total_number, page_length)
        return quotient + int(remainder != 0)


class TaskOperationBase(OperationBase, TaskOperationMixin):
    pass