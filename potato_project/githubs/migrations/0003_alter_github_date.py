# Generated by Django 5.0.7 on 2024-08-01 07:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("githubs", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="github",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
