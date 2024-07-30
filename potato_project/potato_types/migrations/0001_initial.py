# Generated by Django 5.0.7 on 2024-07-28 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PotatoType",
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
                    "potato_name",
                    models.CharField(max_length=255, verbose_name="감자이름"),
                ),
                (
                    "potato_image",
                    models.CharField(max_length=255, verbose_name="감자이미지"),
                ),
                ("potato_description", models.TextField(verbose_name="감자설명")),
            ],
        ),
    ]
