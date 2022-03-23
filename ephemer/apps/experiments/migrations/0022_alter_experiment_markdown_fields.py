import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("experiments", "0021_alter_reportgraphtrace_func"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experiment",
            name="goals",
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="experiment",
            name="description",
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]
