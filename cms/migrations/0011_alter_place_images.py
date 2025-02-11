# Generated by Django 4.2.13 on 2024-09-04 10:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0010_merge_0008_plan_0009_rename_ratings_place_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="images",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="places", to="cms.image"
            ),
        ),
    ]
