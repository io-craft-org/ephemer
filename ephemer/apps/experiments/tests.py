import pytest
from django.urls import reverse

from . import models


# Create your tests here.
@pytest.mark.django_db
def test_experiment_is_created(client):
    data = {"title": "my_exp", "difficulty": 10}
    response = client.post(reverse("experiments-experiment-create"), data=data)

    assert response.status_code == 302

    experiment = models.Experiment.objects.all()[0]
    assert experiment.title == data["title"]


# Create your tests here.
@pytest.mark.django_db
def test_experiment_cbv_is_created(client):
    data = {"title": "my_exp"}
    response = client.post(reverse("experiments-experiment-create-cbv"), data=data)

    assert response.status_code == 302

    experiment = models.Experiment.objects.all()[0]
    assert experiment.title == data["title"]
