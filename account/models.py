from django.db import models
from django.contrib.auth.models import User

# Changes to the built-in User model
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('last_name').null = False


def get_name(self):
    return f"{self.first_name} {self.last_name}"


User.add_to_class("__str__", get_name)
