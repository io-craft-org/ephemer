# Generated by Django 3.2.7 on 2021-12-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiments", "0019_alter_reportdatamanipulation_func"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="participant_count",
            field=models.PositiveIntegerField(
                default=1, verbose_name="Nombre de participants"
            ),
            preserve_default=False,
        ),
    ]
