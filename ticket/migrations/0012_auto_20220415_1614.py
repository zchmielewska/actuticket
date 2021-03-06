# Generated by Django 3.2.13 on 2022-04-15 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0011_auto_20220415_1601'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='finished_at',
            new_name='closed_at',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='finished_by',
        ),
        migrations.AddField(
            model_name='ticket',
            name='closed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='close_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
