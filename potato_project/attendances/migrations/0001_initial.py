# Generated by Django 5.0.7 on 2024-07-24 09:18

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성일자"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="수정일자"),
                ),
                ("date", models.DateField(verbose_name="날짜")),
                ("coin_awarded", models.IntegerField(verbose_name="지급된 코인수")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
