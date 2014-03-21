# coding=utf-8
from django.test import SimpleTestCase as TestCase
from django.test.utils import override_settings
from django_sae.utils.log import RequireInSAE, RequireNotInSAE


class LogTest(TestCase):
    @override_settings(IN_SAE=True)
    def test_require_in_sae(self):
        self.assertTrue(RequireInSAE().filter(None))

    @override_settings(IN_SAE=False)
    def test_require_not_in_sae(self):
        self.assertTrue(RequireNotInSAE().filter(None))
