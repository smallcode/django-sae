# coding=utf-8
from django_sae.contrib.tasks.operations import OperationBase, TaskOperationBase


class OperationMock(OperationBase):
    def post(self):
        return 'foo'


class TaskOperationMock(TaskOperationBase):
    def __init__(self, account):
        super(TaskOperationMock, self).__init__()
        self.account = account

    def post(self):
        pass