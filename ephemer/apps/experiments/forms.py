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


class ParticipantJoinSessionForm(forms.Form):
    pin_code = forms.CharField(
        min_length=models.PIN_CODE_LENGTH,
        max_length=models.PIN_CODE_LENGTH,
    )

    class Meta:
        fields = ["pin_code"]
