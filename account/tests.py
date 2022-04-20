from django.contrib.auth.models import User
from django.test import Client, TestCase


class ExtendedTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def create_user(self):
        user = User.objects.create_user(username="1", email="viewer@example.com", password="pass")
        return user
