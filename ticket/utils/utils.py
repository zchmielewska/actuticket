from django.contrib.auth.models import User
from django.core.mail import send_mail


def send_mail_to_all(subject, message, from_email):
    receivers = []
    for user in User.objects.all():
        receivers.append(user.email)
    send_mail(subject, message, from_email, receivers)

