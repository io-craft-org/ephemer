# Generated by Django 3.2.7 on 2021-09-16 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="experiment",
            name="difficulty",
            field=models.IntegerField(default=0),
        ),
    ]
