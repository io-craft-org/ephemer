import pytest
from django.urls import reverse
from model_bakery.recipe import Recipe
from pytest_django.asserts import assertContains

from . import models


@pytest.mark.django_db
def test_list_experiment(client):
    response = client.get(reverse("experiments-experiment-list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_experiment_details(client):
    experiment = Recipe(models.Experiment).make()
    response = client.get(
        reverse("experiments-experiment-detail", args=(experiment.pk,))
    )
    assert response.status_code == 200
    assertContains(response, experiment.title)
