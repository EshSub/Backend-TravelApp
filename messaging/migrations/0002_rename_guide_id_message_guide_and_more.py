# Generated by Django 4.2.13 on 2024-08-29 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("messaging", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="guide_id",
            new_name="guide",
        ),
        migrations.RenameField(
            model_name="message",
            old_name="place_id",
            new_name="place",
        ),
        migrations.RemoveField(
            model_name="conversation",
            name="user_id",
        ),
        migrations.AddField(
            model_name="conversation",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
