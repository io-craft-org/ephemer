from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiments", "0022_alter_experiment_markdown_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="experiment",
            name="notice",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="experiment",
            name="image",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
