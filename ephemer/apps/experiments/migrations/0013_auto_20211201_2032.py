# Generated by Django 3.2.7 on 2021-12-01 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiments", "0012_auto_20211201_2024"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportgraph",
            name="position",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="reportgraph",
            name="title",
            field=models.CharField(default="", max_length=255),
        ),
    ]
