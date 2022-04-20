from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail


@shared_task
def send_mail_to_all(subject, message, from_email=settings.EMAIL_HOST_USER):
    receivers = []
    for user in User.objects.all():
        receivers.append(user.email)
    send_mail(subject, message, from_email, receivers)
