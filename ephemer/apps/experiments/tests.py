import pytest
from django.urls import reverse
from ephemer.utils import login
from model_bakery.recipe import Recipe
from pytest_django.asserts import assertContains

from . import models


@pytest.mark.django_db
def test_list_experiment_not_accessible_as_guest(client):
    response = client.get(reverse("experiments-experiment-list"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_experiment_accessible_for_staff(client):
    with login(client, is_staff=True):
        response = client.get(reverse("experiments-experiment-list"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_experiment_details_not_accessible_as_guest(client):
    response = client.get(reverse("experiments-experiment-detail", args=(0,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_experiment_details(client):
    experiment = Recipe(models.Experiment).make()
    with login(client, is_staff=True):
        response = client.get(
            reverse("experiments-experiment-detail", args=(experiment.pk,))
        )
    assert response.status_code == 200
    assertContains(response, experiment.title)
