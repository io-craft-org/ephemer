from django import forms

from . import models


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = models.Experiment
        fields = ["title", "description", "goals", "duration_min", "participant_count"]


class SessionCreateForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ["name"]


class SessionJoinForm(forms.Form):
    code = forms.CharField(max_length=5)

    class Meta:
        fields = ["name"]
