import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from ephemer.utils import login
from model_bakery.recipe import Recipe
from pytest_django.asserts import assertContains, assertNotContains
from pytest_mock import mocker

from . import models
from .otree import exceptions as otree_exceptions


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
    with login(client):
        response = client.get(reverse("experiments-session-detail", args=(session.pk,)))
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_session_not_accessible_as_guest(client):
    response = client.get(reverse("experiments-session-create", args=(1,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_session_form(client):
    experiment = Recipe(models.Experiment).make()
    with login(client):
        response = client.get(
            reverse("experiments-session-create", args=(experiment.pk,))
        )
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_session(client, mocker):
    otree_handler = "zz1usouu"

    def mock_call(self, endpoint, data):
        return {
            "admin_url": "http://localhost:8001/SessionStartLinks/zz1usouu",
            "code": otree_handler,
            "session_wide_url": "http://localhost:8001/join/kehikome",
        }

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._call", mock_call
    )

    experiment = Recipe(models.Experiment).make()
    data = {"name": "Test Session"}
    with login(client):
        response = client.post(
            reverse("experiments-session-create", args=(experiment.pk,)), data=data
        )
    assert response.status_code == 302
    session = models.Session.objects.all()[0]
    assert models.Session.objects.count() == 1
    assert session.name == data["name"]
    assert session.otree_handler == otree_handler


@pytest.mark.django_db
def test_create_session_when_backend_down(client, mocker):
    def mock_call(self, endpoint, data):
        raise otree_exceptions.OTreeNotAvailable()

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._call", mock_call
    )

    experiment = Recipe(models.Experiment).make()
    data = {"name": "Test Session"}
    with login(client):
        response = client.post(
            reverse("experiments-session-create", args=(experiment.pk,)), data=data
        )
    assert response.status_code == 302
    assert models.Session.objects.count() == 0


##
# Service
##
def test_service_unavailable_page(client):
    response = client.get(reverse("experiments-service-unavailable"))
    assert response.status_code == 200
