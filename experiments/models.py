from django.db import models
from django.shortcuts import reverse


# Create your models here.
class Experiment(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="Titre", help_text="Le titre de l'expérience"
    )
    difficulty = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse(
            "experiments-experiment-detail", kwargs={"experiment_id": self.pk}
        )
