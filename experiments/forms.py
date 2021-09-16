from django import forms

from . import models


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = models.Experiment
        fields = ["title", "difficulty"]
