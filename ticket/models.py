from django.conf import settings
from django.db import models
from datetime import date

STATUS = (
    (1, "new"),
    (2, "in progress"),
    (3, "closed"),
)


class Model(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"


class Type(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    written_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="write_user")
    written_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


class Ticket(models.Model):
    model = models.ManyToManyField(Model)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    version = models.CharField(max_length=128)
    year = models.PositiveIntegerField(default=date.today().year, verbose_name="reporting year")
    month = models.PositiveIntegerField(default=date.today().month-1, verbose_name="reporting month")
    deadline = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="create_user")
    created_at = models.DateTimeField(auto_now=True)
    undertook_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="undertake_user", null=True)
    undertook_at = models.DateTimeField(null=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="close_user", null=True)
    closed_at = models.DateTimeField(null=True)
    status = models.IntegerField(choices=STATUS, default=1)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-id"]
