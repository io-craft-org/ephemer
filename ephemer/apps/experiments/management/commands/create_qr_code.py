import os
from urllib.parse import urljoin

import qrcode
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from ephemer.apps import experiments


class Command(BaseCommand):
    help = "Crée le QR code pointant sur la page pour rejoindre une session."

    def handle(self, *args, **options):

        hostname = settings.EPHEMER_HOSTNAME
        path = urljoin(hostname, reverse("experiments-participant-join-session"))

        img = qrcode.make(path)

        app_path = os.path.split(experiments.__file__)[0]
        static_img_path = os.path.join(app_path, "static/img")
        os.makedirs(static_img_path, exist_ok=True)
        qr_code_img_path = os.path.join(static_img_path, "join-session-qr-code.png")

        self.stdout.write(
            f"Creating and saving the qr code pointing at {path} in the app's static directory."
        )

        img.save(qr_code_img_path)

        self.stdout.write("qr code created successfully.")
