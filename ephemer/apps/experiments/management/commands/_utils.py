import os
import shutil

from django.conf import settings
from django.core.management import call_command

from ephemer.apps import experiments


def get_this_app_path():
    return os.path.split(experiments.__file__)[0]


def copy_directory_content_to_media_root(command, dirname, media_path=""):
    media_root = os.path.join(settings.MEDIA_ROOT, media_path)
    if not os.path.exists(media_root):
        os.mkdir(media_root)
    content_path = os.path.join(get_this_app_path(), dirname, media_path)
    command.stdout.write(
        f"Installing content from {content_path} in MEDIA_ROOT ({media_root})"
    )
    filenames = os.listdir(content_path)
    if filenames:
        filenames.sort()
    media_dirs = []
    for f in filenames:
        full_path = os.path.join(content_path, f)
        if os.path.isdir(full_path):
            media_dirs.append(f)
        else:
            shutil.copy(full_path, media_root)
            command.stdout.write(f"- copied content file '{f}'")
    for media_dir in media_dirs:
        copy_directory_content_to_media_root(
            command, dirname, media_path=os.path.join(media_path, media_dir)
        )


def load_data_from(command, filename):
    filepath = os.path.join(get_this_app_path(), filename)
    command.stdout.write(f"Loading data from {filepath}")
    call_command("loaddata", filepath)
    command.stdout.write("Data loaded")


def is_there_data_already():
    from ephemer.apps.experiments.models import Experiment

    return Experiment.objects.exists()
