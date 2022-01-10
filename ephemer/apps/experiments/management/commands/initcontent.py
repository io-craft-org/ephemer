import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ephemer.apps import experiments


class Command(BaseCommand):
    help = "Installe le contenu initial de l'app experiments (notices PDF, images)"

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        app_path = os.path.split(experiments.__file__)[0]

        self.stdout.write(
            f"Installing content of 'experiments' in MEDIA_ROOT ({media_root})"
        )
        content_path = os.path.join(app_path, "initial_content")
        filenames = os.listdir(content_path)
        for f in filenames:
            shutil.copy(os.path.join(content_path, f), media_root)
            self.stdout.write(f"- copied content file '{f}'")

        self.stdout.write("Loading initial data for the 'experiments' app")
        call_command(
            "loaddata", os.path.join(app_path, "initial_experiments_data.json")
        )
        self.stdout.write("Initial data loaded")
