from django.db import models
from django.shortcuts import reverse


class ExperimentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("title")


class Experiment(models.Model):
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

    def get_absolute_url(self):
        return reverse(
            "experiments-experiment-detail", kwargs={"experiment_id": self.pk}
        )


class Session(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    name = models.CharField(default="Session Sans Nom", max_length=100)
