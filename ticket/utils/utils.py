import os

from django.contrib.auth.models import User
from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


def send_mail_to_all(subject, message, from_email=os.getenv("EMAIL_HOST_USER")):
    receivers = []
    for user in User.objects.all():
        receivers.append(user.email)
    send_mail(subject, message, from_email, receivers)
