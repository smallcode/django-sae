# coding=utf-8
from django_sae.contrib.tasks.cron import OperationView
from django_sae.contrib.tasks.operations import TaskOperationMixin
from django_sae.contrib.tasks.tests.base import CronViewTestMixin


class CronViewTest(CronViewTestMixin):
    urls = 'django_sae.contrib.tasks.tests.urls'

    def test_router_return_none(self):
        response = self.client.get('/mock')
        self.assertResult(response, 3)

    def test_as_task(self):
        r = OperationView.as_task(TaskOperationMixin())
        self.assertEqual(len(r), 1)

    def test_as_task_with_none(self):
        r = OperationView.as_task(None)
        self.assertEqual(len(r), 0)

    def test_get_operation(self):
        view = OperationView()
        self.assertRaises(NotImplementedError, view.get_operation, None)