# Generated by Django 5.0.7 on 2024-07-19 06:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_remove_user_exp_remove_user_level_user_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="birthday",
        ),
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
        migrations.AlterField(
            model_name="user",
            name="baekjoon_id",
            field=models.CharField(default="", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=128, verbose_name="password"),
        ),
    ]

