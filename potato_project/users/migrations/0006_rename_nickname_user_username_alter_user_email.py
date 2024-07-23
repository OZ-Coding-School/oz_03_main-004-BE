# Generated by Django 5.0.7 on 2024-07-21 16:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_remove_user_birthday_remove_user_name_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="nickname",
            new_name="username",
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
