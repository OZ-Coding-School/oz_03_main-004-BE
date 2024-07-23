# Generated by Django 5.0.7 on 2024-07-18 01:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_birthday"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="description",
        ),
        migrations.RemoveField(
            model_name="user",
            name="login_type",
        ),
        migrations.AddField(
            model_name="user",
            name="exp",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="level",
            field=models.IntegerField(default=0),
        ),
    ]