# Generated by Django 3.2.7 on 2021-10-20 18:41

from django.db import migrations, models

import ephemer.apps.experiments.models


class Migration(migrations.Migration):

    dependencies = [
        ("experiments", "0007_experiment_otree_app_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="participant_code",
            field=models.CharField(
                default=ephemer.apps.experiments.models.generate_pin, max_length=5
            ),
        ),
    ]
