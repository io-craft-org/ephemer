import os
import random

from django.conf import settings
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
    pin_code = models.CharField(max_length=PIN_CODE_LENGTH, default=generate_pin)
    join_in_code = models.CharField(default="", max_length=50)
    csv = models.FilePathField(
        path=get_csv_path,
        null=True,
        blank=True,
    )


class ReportTemplate(models.Model):
    """A report template for a given Experiment"""

    experiment = models.OneToOneField(
        Experiment, on_delete=models.CASCADE, related_name="report_template"
    )

    def __str__(self):
        return f"Report for <{self.experiment.title}>"


class ReportDataManipulation(models.Model):
    title = models.CharField(max_length=255)
    data_name = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=0)
    report = models.ForeignKey(
        ReportTemplate, on_delete=models.CASCADE, related_name="data_manipulations"
    )
    func = models.CharField(max_length=255, choices=[("mean", "Moyenne")])
    columns = models.JSONField(default=list)

    def __str__(self):
        return f"Data Manipulation <{self.title}> for <{self.report.experiment.title}>"


class ReportGraph(models.Model):
    title = models.CharField(max_length=255, default="")
    position = models.PositiveIntegerField(default=0)
    report = models.ForeignKey(
        ReportTemplate, on_delete=models.CASCADE, related_name="graphs"
    )
    x_tick_labels = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"Graph <{self.title}> for <{self.report.experiment.title}>"


class ReportGraphTrace(models.Model):
    graph = models.ForeignKey(
        ReportGraph, on_delete=models.CASCADE, related_name="traces"
    )
    x = models.CharField(max_length=255)
    y = models.CharField(max_length=255, null=True, blank=True)
    func = models.CharField(max_length=255, choices=[("avg", "Moyenne")])
    name = models.CharField(max_length=255)
