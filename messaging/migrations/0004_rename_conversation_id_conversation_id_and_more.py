# Generated by Django 4.2.13 on 2024-09-03 14:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("messaging", "0003_alter_conversation_isai"),
    ]

    operations = [
        migrations.RenameField(
            model_name="conversation",
            old_name="conversation_id",
            new_name="id",
        ),
        migrations.AlterField(
            model_name="message",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
