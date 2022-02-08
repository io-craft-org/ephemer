from django.core.management.base import BaseCommand


from .utils import copy_directory_content_to_media_root, load_data_from


class Command(BaseCommand):
    help = "Installe le contenu de test de l'app experiments (fausses sessions avec résultats)"

    def handle(self, *args, **options):
        copy_directory_content_to_media_root(command=self, dirname="test_content")
        load_data_from(command=self, filename="experiments_test_data.json")
