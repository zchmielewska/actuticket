from django.contrib import admin

from ticket import models


@admin.register(models.Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


