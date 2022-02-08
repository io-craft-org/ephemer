from django.core.management.base import BaseCommand


from .utils import (
    copy_directory_content_to_media_root,
    load_data_from,
    is_there_data_already,
)


class Command(BaseCommand):
    help = "Installe le contenu de test de l'app experiments (fausses sessions avec résultats)"

    def handle(self, *args, **options):
        if is_there_data_already():
            self.stdout.write(
                "Installation du contenu de test annulée. Des données sont déjà présentes."
            )
            return
        copy_directory_content_to_media_root(command=self, dirname="test_content")
        load_data_from(command=self, filename="experiments_test_data.json")
