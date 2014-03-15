# coding=utf-8
from django.test import SimpleTestCase
from django.conf import settings
from django_sae.conf import settings as sae_settings


class SettingsTestCase(SimpleTestCase):
    def test_settings(self):
        self.assertEqual(settings.IN_SAE, sae_settings.IN_SAE)
        self.assertEqual(settings.STATIC_URL, sae_settings.STATIC_URL)
        self.assertEqual(settings.TIME_ZONE, sae_settings.TIME_ZONE)
        self.assertEqual(settings.USE_TZ, sae_settings.USE_TZ)
        self.assertEqual(settings.LANGUAGE_CODE, sae_settings.LANGUAGE_CODE)
        self.assertEqual(settings.USE_I18N, sae_settings.USE_I18N)

