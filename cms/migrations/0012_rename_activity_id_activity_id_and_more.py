# Generated by Django 4.2.13 on 2024-09-04 10:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0011_alter_place_images"),
    ]

    operations = [
        migrations.RenameField(
            model_name="activity",
            old_name="activity_id",
            new_name="id",
        ),
        migrations.RenameField(
            model_name="activity",
            old_name="activity_name",
            new_name="name",
        ),
    ]
