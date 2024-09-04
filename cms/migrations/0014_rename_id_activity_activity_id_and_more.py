# Generated by Django 4.2.13 on 2024-09-04 10:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0013_rename_place_id_place_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="activity",
            old_name="id",
            new_name="activity_id",
        ),
        migrations.RenameField(
            model_name="activity",
            old_name="name",
            new_name="activity_name",
        ),
        migrations.RenameField(
            model_name="place",
            old_name="id",
            new_name="place_id",
        ),
        migrations.RenameField(
            model_name="place",
            old_name="name",
            new_name="place_name",
        ),
    ]
