# Generated by Django 3.2.13 on 2022-04-14 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_auto_20220414_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='claimed_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='finished_at',
            field=models.DateTimeField(null=True),
        ),
    ]
