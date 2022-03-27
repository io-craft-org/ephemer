import random

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField


class ExperimentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("title")


class Experiment(models.Model):
    """
    An available experiment that can be turned into a session using a
    configuration.
    """

    DEFAULT_MAXIMUM_PARTICIPANT_COUNT = 1000

    objects = ExperimentManager()

    title = models.CharField(
        max_length=255, verbose_name="Titre", help_text="Le titre de l'expérience"
    )
    goals = MarkdownxField(blank=True, null=True)
    description = MarkdownxField(blank=True, null=True)
    duration_min = models.PositiveIntegerField(
        verbose_name="Durée", help_text="En minutes"
    )
    participant_count = models.PositiveIntegerField(
        verbose_name="Nombre de participants"
    )
    participants_per_group = models.PositiveIntegerField(
        verbose_name="Nombre de participants par groupe", blank=True, null=True
    )

    maximum_participant_count = models.PositiveIntegerField(
        verbose_name="Nombre maximum de participants", null=True
    )

    otree_app_name = models.CharField(
        max_length=50, verbose_name="Nom de l'application oTree"
    )

    notice = models.FileField(blank=True, null=True)

    image = models.FileField(blank=True, null=True)

    report_script = models.CharField(max_length=200, blank=True, null=True)

    slug = models.CharField(max_length=30)

    def get_absolute_url(self):
        return reverse(
            "experiments-experiment-detail", kwargs={"experiment_id": self.pk}
        )

    def __str__(self):
        return self.title


PIN_CODE_LENGTH = 5


def generate_pin():
    return f"{random.randrange(1, 10**PIN_CODE_LENGTH):0{PIN_CODE_LENGTH}}"


def get_csv_path():
    return f"{settings.MEDIA_ROOT}/sessions/exports/"


class Session(models.Model):
    """A Session represents an instance of an experiment on the oTree side"""

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sessions"
    )
    created_on = models.DateTimeField(
        default=timezone.now, verbose_name="date de création"
    )
    name = models.CharField(default="Session Sans Nom", max_length=100)
    participant_count = models.PositiveIntegerField(
        verbose_name="Nombre de participants"
    )
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    otree_handler = models.CharField(max_length=50)
    pin_code = models.CharField(
        unique=True, max_length=PIN_CODE_LENGTH, default=generate_pin
    )
    join_in_code = models.CharField(default="", max_length=50)
    csv = models.FilePathField(
        path=get_csv_path,
        null=True,
        blank=True,
    )
