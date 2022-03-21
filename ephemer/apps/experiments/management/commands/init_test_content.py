import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


from .utils import (
    copy_directory_content_to_media_root,
    load_data_from,
)


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Installe le contenu de test de l'app experiments (fausses sessions avec résultats)"

    def handle(self, *args, **options):
        copy_directory_content_to_media_root(command=self, dirname="test_content")
        try:
            load_data_from(command=self, filename="experiments_test_data.json")
        except IntegrityError as error:
            LOGGER.error(error)
            self.stdout.write(
                "Installation du contenu de test annulée. Des données sont déjà présentes."
            )
