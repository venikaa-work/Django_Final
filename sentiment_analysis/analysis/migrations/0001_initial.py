# Generated by Django 4.2.16 on 2024-09-17 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Record",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("chat_file", models.CharField(max_length=10000)),
                ("sentiment_score", models.CharField(max_length=50)),
            ],
        ),
    ]
