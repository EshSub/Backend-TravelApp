# Generated by Django 4.2.13 on 2024-08-30 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0007_alter_place_accommodation_places_nearby"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("image", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="place",
            name="ratings",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="place",
            name="header_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="cms.image",
            ),
        ),
        migrations.AddField(
            model_name="place",
            name="images",
            field=models.ManyToManyField(related_name="places", to="cms.image"),
        ),
    ]
