# Generated by Django 3.2.13 on 2022-04-15 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0013_auto_20220415_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='ticket',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket'),
            preserve_default=False,
        ),
    ]
