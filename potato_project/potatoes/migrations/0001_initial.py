# Generated by Django 5.0.7 on 2024-07-28 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("potato_types", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Potato",
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
                ("is_acquired", models.BooleanField(blank=True, null=True)),
                ("is_selected", models.BooleanField(blank=True, null=True)),
                (
                    "potato_type_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="potato_types.potatotype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
