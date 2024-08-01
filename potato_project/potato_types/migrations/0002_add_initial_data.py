from django.db import migrations


def insert_initial_data(apps, schema_editor):
    PotatoType = apps.get_model("potato_types", "PotatoType")
    PotatoType.objects.create(
        potato_name="levelOnePotato",
        potato_description="Can be obtained after level 1.",
    )
    PotatoType.objects.create(
        potato_name="levelTwoPotato",
        potato_description="Can be obtained after level 2.",
    )
    PotatoType.objects.create(
        potato_name="levelThreePotato",
        potato_description="Can be obtained after level 3.",
    )
    PotatoType.objects.create(
        potato_name="levelFourPotato",
        potato_description="Can be obtained after level 4.",
    )
    PotatoType.objects.create(
        potato_name="levelFivePotato",
        potato_description="Can be obtained after level 5.",
    )
    PotatoType.objects.create(
        potato_name="winterPotato",
        potato_description="Can be obtained by committing on Christmas Day.",
    )
    PotatoType.objects.create(
        potato_name="ghostPotato",
        potato_description="Can be obtained by committing on Halloween.",
    )
    PotatoType.objects.create(
        potato_name="crystalPotato",
        potato_description="Can be obtained by committing consecutively for a month.",
    )
    PotatoType.objects.create(
        potato_name="dirtyPotato",
        potato_description="Can be obtained if there are no commits for a month.",
    )
    PotatoType.objects.create(
        potato_name="greenPotato",
        potato_description="Can be obtained if there are no commits for 3 months.",
    )
    PotatoType.objects.create(potato_name="shPotato", potato_description="?")


class Migration(migrations.Migration):
    dependencies = [
        ("potato_types", "0001_initial"),  # "0001_initial"은 모델 생성 마이그레이션의 이름입니다.
    ]

    operations = [
        migrations.RunPython(insert_initial_data),
    ]
