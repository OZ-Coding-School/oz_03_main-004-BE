# Generated by Django 5.0.7 on 2024-07-27 18:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.CharField(default="", max_length=255, null=True),
        ),
    ]
