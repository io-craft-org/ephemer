from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone


class ExperimentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("title")


class Experiment(models.Model):
    """
    An available experiment that can be turned into a session using a
    configuration.
    """

    objects = ExperimentManager()

    title = models.CharField(
        max_length=255, verbose_name="Titre", help_text="Le titre de l'expérience"
    )
    description = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    duration_min = models.PositiveIntegerField(
        verbose_name="Durée", help_text="En minutes"
    )
    participant_count = models.PositiveIntegerField(
        verbose_name="Nombre de participants"
    )

    otree_app_name = models.CharField(
        max_length=50, verbose_name="Nom de l'application oTree"
    )

    def get_absolute_url(self):
        return reverse(
            "experiments-experiment-detail", kwargs={"experiment_id": self.pk}
        )


class Session(models.Model):
    """A Session represents an instance of an experiment on the oTree side"""

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sessions"
    )
    created_on = models.DateTimeField(
        default=timezone.now, verbose_name="date de création"
    )
    name = models.CharField(default="Session Sans Nom", max_length=100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    otree_handler = models.CharField(max_length=50)
