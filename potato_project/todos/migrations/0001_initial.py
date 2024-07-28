# Generated by Django 5.0.7 on 2024-07-28 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Todo",
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
                ("task", models.CharField(max_length=50)),
                ("is_done", models.BooleanField(default=False)),
                ("date", models.DateTimeField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
