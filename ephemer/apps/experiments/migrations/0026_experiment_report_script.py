# Generated by Django 3.2.7 on 2022-01-31 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiments", "0025_experiment_participants_per_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="experiment",
            name="report_script",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
