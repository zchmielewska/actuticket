# Generated by Django 3.2.13 on 2022-04-12 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('written_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('written_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='write_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(default=2022)),
                ('month', models.PositiveIntegerField(default=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('claimed_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(1, 'new'), (2, 'running'), (3, 'finished')])),
                ('claimed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claim_user', to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.comment')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_user', to=settings.AUTH_USER_MODEL)),
                ('model', models.ManyToManyField(to='ticket.Model')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.type')),
            ],
        ),
    ]
