# Generated by Django 3.2.7 on 2021-10-13 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiments', '0004_auto_20211013_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date de création'),
        ),
    ]
