import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from ephemer.utils import login
from model_bakery.recipe import Recipe
from pytest_django.asserts import assertContains, assertNotContains

from . import models


######
# Experiments
######
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
    experiment = Recipe(models.Experiment, title="My Exp").make()
    with login(client, is_staff=True):
        response = client.get(
            reverse("experiments-experiment-detail", args=(experiment.pk,))
        )
    assert response.status_code == 200
    assertContains(response, experiment.title)


#####
# Sessions
#####
@pytest.mark.django_db
def test_list_sessions_not_accessible_as_guest(client):
    response = client.get(reverse("experiments-session-list"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_session_are_only_mine(client):
    other_session = Recipe(models.Session, name="Other Session").make()

    with login(client, is_staff=True) as user:
        my_session = Recipe(models.Session, name="My session", created_by=user).make()
        response = client.get(reverse("experiments-session-list"))

    assertNotContains(response, other_session.name)
    assertContains(response, my_session.name)
    assert response.status_code == 200


@pytest.mark.django_db
def test_session_details_not_accessible_as_guest(client):
    session = Recipe(models.Session).make()
    response = client.get(reverse("experiments-session-detail", args=(session.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_owner_can_view_session_details(client):
    with login(client, is_staff=True) as user:
        session = Recipe(models.Session, created_by=user).make()
        response = client.get(reverse("experiments-session-detail", args=(session.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_cannot_see_other_people_session_details(client):
    session = Recipe(models.Session).make()
    with login(client, is_staff=True):
        response = client.get(reverse("experiments-session-detail", args=(session.pk,)))
    assert response.status_code == 404
