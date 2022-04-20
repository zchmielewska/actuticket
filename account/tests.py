from django.contrib import auth
from django.contrib.auth.models import User
from django.test import Client, TestCase


class ExtendedTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def create_user(self):
        user = User.objects.create_user(username="1", email="user@example.com", password="pass")
        return user


class TestRegisterView(ExtendedTestCase):
    def test_get(self):
        response = self.client.get("/account/register/")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.assertEqual(User.objects.count(), 0)

        data = {
            "email": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "HJk&ui34",
            "password2": "HJk&ui34",
        }

        response = self.client.post("/account/register/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)


class TestLoginView(ExtendedTestCase):
    def test_get(self):
        response = self.client.get("/account/login/")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.create_user()
        response = self.client.post("/account/login/", {"email": "user@example.com", "password": "pass"})
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
