# coding=utf-8
from django_sae.contrib.tasks.cron import OperationView
from django_sae.contrib.tasks.operations import TaskOperationMixin


class OperationViewMock(OperationView):
    def get_operation(self, request):
        return [TaskOperationMixin() for _ in range(0, 3)]