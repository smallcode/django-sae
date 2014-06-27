# coding=utf-8
from django.test import TestCase
from tests.models import User


class ModelsTest(TestCase):
    def test_user(self):
        user = User()
        user.save()
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertEqual(str(user), '1')