# Generated by Django 3.2.13 on 2022-04-15 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_alter_ticket_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='version',
            field=models.CharField(max_length=128),
        ),
    ]
