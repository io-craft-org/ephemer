from django.core.management.base import BaseCommand

from .utils import copy_directory_content_to_media_root, load_data_from


class Command(BaseCommand):
    help = "Installe le contenu initial de l'app experiments (notices PDF, images)"

    def handle(self, *args, **options):
        copy_directory_content_to_media_root(command=self, dirname="initial_content")
        load_data_from(command=self, filename="initial_experiments_data.json")
