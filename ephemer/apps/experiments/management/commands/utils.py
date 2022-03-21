import os
import shutil

from django.conf import settings
from django.core.management import call_command
from ephemer.apps import experiments


def get_this_app_path():
    return os.path.split(experiments.__file__)[0]


def copy_directory_content_to_media_root(command, dirname):
    media_root = settings.MEDIA_ROOT
    content_path = os.path.join(get_this_app_path(), dirname)
    command.stdout.write(
        f"Installing content from {content_path} in MEDIA_ROOT ({media_root})"
    )
    filenames = os.listdir(content_path)
    for f in filenames:
        shutil.copy(os.path.join(content_path, f), media_root)
        command.stdout.write(f"- copied content file '{f}'")


def load_data_from(command, filename):
    filepath = os.path.join(get_this_app_path(), filename)
    command.stdout.write(f"Loading data from {filepath}")
    call_command("loaddata", filepath)
    command.stdout.write("Data loaded")


def is_there_data_already():
    from ephemer.apps.experiments.models import Experiment

    return Experiment.objects.exists()
