import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase

from ticket import models


class ExtendedTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def create_and_log_user(self):
        user = User.objects.create(username="1", email="user@example.com")
        self.client.force_login(user)
        return user

    def log_user(self, pk):
        user = User.objects.get(pk=pk)
        self.client.force_login(user)
        return user


class TestMainView(ExtendedTestCase):
    def test_get(self):
        # Log-in is required
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/login?next=/")

        self.create_and_log_user()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        # Main page shows list of tickets
        self.assertEqual(len(response.context.get("tickets")), 0)


class TestMainViewFix01(ExtendedTestCase):
    fixtures = ["01.json"]

    def test_get(self):
        self.log_user(pk=1)
        response = self.client.get("/")
        self.assertEqual(len(response.context.get("tickets")), 1)


class TestMainViewFix02(ExtendedTestCase):
    fixtures = ["02.json"]

    def test_get(self):
        # Pagination uses 15 tickets per page
        self.log_user(pk=1)
        response = self.client.get("/")
        self.assertEqual(len(response.context.get("tickets")), 15)
        response = self.client.get("/?page=2")
        self.assertEqual(len(response.context.get("tickets")), 1)


class TestAddTicketView(ExtendedTestCase):
    def test_get(self):
        response = self.client.get("/add/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/login?next=/add/")

        self.create_and_log_user()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class TestAddTicketViewFix01(ExtendedTestCase):
    fixtures = ["01.json"]

    def test_post(self):
        user = self.log_user(pk=1)
        tickets = models.Ticket.objects.all()
        self.assertEqual(len(tickets), 1)
        data = {
            "model": [1],
            "type": 1,
            "version": "1-50",
            "year": 2022,
            "month": 12,
            "deadline": "2022-04-05 06:00Z",
            "created_by": user,
            "created_at": datetime.datetime.now()
        }
        response = self.client.post("/add/", data)
        self.assertEqual(response.status_code, 302)
        tickets = models.Ticket.objects.all()
        self.assertEqual(len(tickets), 2)


class TestUndertakeTicketViewFix01(ExtendedTestCase):
    fixtures = ["01.json"]

    def test_get(self):
        ticket = models.Ticket.objects.get(pk=1)
        self.assertEqual(ticket.status, 1)

        response = self.client.get("/ticket/undertake/1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/login?next=/ticket/undertake/1")
        user = self.log_user(pk=1)
        response = self.client.get("/ticket/undertake/1")
        self.assertEqual(response.status_code, 302)

        ticket = models.Ticket.objects.get(pk=1)
        self.assertEqual(ticket.status, 2)
        self.assertEqual(ticket.undertook_by, user)


class TestTicketDetailViewFix01(ExtendedTestCase):
    fixtures = ["01.json"]

    def test_get(self):
        response = self.client.get("/ticket/1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/login?next=/ticket/1")
        self.log_user(pk=1)
        response = self.client.get("/ticket/1")
        self.assertEqual(response.status_code, 200)


class TestCloseTicketViewFix01(ExtendedTestCase):
    fixtures = ["03.json"]

    def test_get(self):
        ticket = models.Ticket.objects.get(pk=1)
        self.assertEqual(ticket.status, 2)

        response = self.client.get("/ticket/close/1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/login?next=/ticket/close/1")
        user = self.log_user(pk=1)
        response = self.client.get("/ticket/close/1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/ticket/1")

        ticket = models.Ticket.objects.get(pk=1)
        self.assertEqual(ticket.status, 3)
        self.assertEqual(ticket.closed_by, user)


class TestAddCommentViewFix01(ExtendedTestCase):
    fixtures = ["01.json"]

    def test_get(self):
        response = self.client.get("/ticket/comment/1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/login?next=/ticket/comment/1")
        user = self.log_user(pk=1)
        response = self.client.get("/ticket/comment/1")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        ticket = models.Ticket.objects.get(pk=1)
        comments = models.Comment.objects.filter(ticket=ticket)
        self.assertEqual(len(comments), 0)

        user = self.log_user(pk=1)
        data = {
            "ticket": 1,
            "message": "Test comment",
        }
        response = self.client.post("/ticket/comment/1", data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/ticket/1")

        comments = models.Comment.objects.filter(ticket=ticket)
        self.assertEqual(len(comments), 1)
