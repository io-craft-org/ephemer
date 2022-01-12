from django import forms
from django.core.exceptions import ValidationError

from . import models


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = models.Experiment
        fields = ["title", "description", "goals", "duration_min", "participant_count"]


class SessionCreateForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = ["name", "participant_count"]

    def __init__(self, *args, experiment: models.Experiment, **kwargs):
        super().__init__(*args, **kwargs)
        if experiment.participants_per_group:
            number_input = forms.NumberInput(
                attrs={"step": experiment.participants_per_group}
            )
            self.fields["participant_count"] = forms.IntegerField(
                widget=number_input,
                min_value=experiment.participants_per_group,
                error_messages={
                    "min_value": "Le nombre de participants doit être au minimum de la taille d'un groupe."
                },
                label="Nombre de participants",
            )
        else:
            self.fields["participant_count"] = forms.IntegerField(
                min_value=1,
                error_messages={"min_value": "Il doit y avoir au moins un participant"},
                label="Nombre de participants",
            )

    def clean_participant_count(self):
        widget = self.fields["participant_count"].widget
        step = widget.attrs.get("step", None)
        value = self.cleaned_data["participant_count"]
        if step and value % step != 0:
            raise ValidationError(
                f"Le nombre de participants doit être un multiple de {step}."
            )
        return value


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
