import json
import tempfile
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from ephemer.utils import login
from model_bakery.recipe import Recipe
from pytest_django.asserts import assertContains, assertNotContains
from pytest_mock import mocker

from . import models
from .otree import exceptions as otree_exceptions
from .otree.connector import OTreeConnector


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

    with login(client, is_staff=False) as user:
        my_session = Recipe(models.Session, name="My session", created_by=user).make()
        response = client.get(reverse("experiments-session-list"))

    assertNotContains(response, other_session.name)
    assertContains(response, my_session.name)
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_all_sessions_if_staff(client):
    other_session = Recipe(models.Session, name="Other Session").make()

    with login(client, is_staff=True) as user:
        my_session = Recipe(models.Session, name="My session", created_by=user).make()
        response = client.get(reverse("experiments-session-list"))

    assertContains(response, other_session.name)
    assertContains(response, my_session.name)
    assert response.status_code == 200


@pytest.mark.django_db
def test_session_details_not_accessible_as_guest(client):
    session = Recipe(models.Session).make()
    response = client.get(reverse("experiments-session-detail", args=(session.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_owner_can_view_session_details(client, mocker):
    def mock_get(self, endpoint, data={}):
        return {
            "REAL_WORLD_CURRENCY_CODE": "USD",
            "admin_url": "http://localhost:8001/SessionStartLinks/93r6k4ov",
            "config": {
                "app_sequence": ["survey", "payment_info"],
                "display_name": "survey",
                "doc": "",
                "name": "survey",
                "num_demo_participants": 1,
                "participation_fee": 0.0,
                "real_world_currency_per_point": 1.0,
            },
            "num_participants": 3,
            "participants": [
                {
                    "code": "3cro7uw4",
                    "id_in_session": 1,
                    "label": None,
                    "payoff_in_real_world_currency": 0.0,
                },
                {
                    "code": "rg77qgh9",
                    "id_in_session": 2,
                    "label": None,
                    "payoff_in_real_world_currency": 0.0,
                },
                {
                    "code": "a8wx034q",
                    "id_in_session": 3,
                    "label": None,
                    "payoff_in_real_world_currency": 0.0,
                },
            ],
            "session_wide_url": "http://localhost:8001/join/juvutiru",
        }

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._get", mock_get
    )

    with login(client, is_staff=False) as user:
        session = Recipe(models.Session, created_by=user).make()
        response = client.get(reverse("experiments-session-detail", args=(session.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_can_view_any_session_details(client, mocker):
    def mock_get(self, endpoint, data={}):
        return {
            "REAL_WORLD_CURRENCY_CODE": "USD",
            "admin_url": "http://localhost:8001/SessionStartLinks/93r6k4ov",
            "config": {
                "app_sequence": ["survey", "payment_info"],
                "display_name": "survey",
                "doc": "",
                "name": "survey",
                "num_demo_participants": 1,
                "participation_fee": 0.0,
                "real_world_currency_per_point": 1.0,
            },
            "num_participants": 3,
            "participants": [
                {
                    "code": "3cro7uw4",
                    "id_in_session": 1,
                    "label": None,
                    "payoff_in_real_world_currency": 0.0,
                },
                {
                    "code": "rg77qgh9",
                    "id_in_session": 2,
                    "label": None,
                    "payoff_in_real_world_currency": 0.0,
                },
                {
                    "code": "a8wx034q",
                    "id_in_session": 3,
                    "label": None,
                    "payoff_in_real_world_currency": 0.0,
                },
            ],
            "session_wide_url": "http://localhost:8001/join/juvutiru",
        }

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._get", mock_get
    )

    session = Recipe(models.Session).make()

    with login(client, is_staff=True):
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

    def mock_post(self, endpoint, data):
        return {
            "admin_url": "http://localhost:8001/SessionStartLinks/zz1usouu",
            "code": otree_handler,
            "session_wide_url": "http://localhost:8001/join/kehikome",
        }

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._post", mock_post
    )

    experiment = Recipe(models.Experiment, participant_count=1).make()
    data = {"name": "Test Session", "participant_count": 1}
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
    def mock_post(self, endpoint, data):
        raise otree_exceptions.OTreeNotAvailable()

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._post", mock_post
    )

    experiment = Recipe(models.Experiment, participant_count=1).make()
    data = {"name": "Test Session", "participant_count": 1}
    with login(client):
        response = client.post(
            reverse("experiments-session-create", args=(experiment.pk,)), data=data
        )
    assert response.status_code == 302
    assert models.Session.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_delete_other_session(client):
    session = Recipe(models.Session).make()

    with login(client):
        response = client.get(reverse("experiments-session-delete", args=(session.pk,)))
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_can_delete_own_session(client):
    with login(client) as user:
        session = Recipe(models.Session, created_by=user).make()
        response = client.post(
            reverse("experiments-session-delete", args=(session.pk,))
        )

    assert models.Session.objects.count() == 0
    assert response.status_code == 302


@pytest.mark.django_db
def test_staff_can_delete_session(client):
    session = Recipe(models.Session).make()
    with login(client, is_staff=True):
        response = client.post(
            reverse("experiments-session-delete", args=(session.pk,))
        )

    assert models.Session.objects.count() == 0
    assert response.status_code == 302


@pytest.mark.django_db
def test_session_is_joinable_by_anyone(client):
    session = Recipe(models.Session).make()
    response = client.get(reverse("experiments-session-join", args=(session.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_guest_can_join_session(client):
    pin_code = "12345"
    join_in_code = "abcdef"
    Recipe(models.Session, pin_code=pin_code, join_in_code=join_in_code).make()
    response = client.post(
        reverse("experiments-participant-join-session"), data={"pin_code": pin_code}
    )
    assert response.status_code == 302
    assert join_in_code in response.url


@pytest.mark.django_db
def test_guest_input_wrong_pin(client):
    wrong_pin_code = "12345"
    Recipe(models.Session).make()
    response = client.post(
        reverse("experiments-participant-join-session"),
        data={"pin_code": wrong_pin_code},
    )
    assert response.status_code == 200


##
# JSON
##
@pytest.mark.django_db
def test_session_participants_state_json_not_accessible_as_guest(client):
    session = Recipe(models.Session).make()
    response = client.get(
        reverse("experiments-session-participants-state-json", args=(session.pk,))
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_session_participants_state_json_not_accessible_if_not_owner(client):
    user = Recipe(User).make()
    session = Recipe(models.Session, created_by=user).make()
    with login(client):
        response = client.get(
            reverse("experiments-session-participants-state-json", args=(session.pk,))
        )
    assert response.status_code == 404


@pytest.mark.django_db
def test_owner_can_access_session_participants_state_json_endpoint(client, mocker):
    def mock_get(self, endpoint, data={}):
        return [
            {
                "_numeric_label": "P1",
                "code": "1votfepp",
                "label": None,
                "_current_page": "2/20",
                "_current_app_name": "FGES_Louvain",
                "_round_number": 1,
                "_current_page_name": "Test1_Page",
                "_monitor_note": None,
                "_last_page_timestamp": 1635954202,
                "id_in_session": 1,
            }
        ]

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._get", mock_get
    )

    with login(client) as user:
        session = Recipe(models.Session, created_by=user).make()
        response = client.get(
            reverse("experiments-session-participants-state-json", args=(session.pk,))
        )
    assert response.status_code == 200


########################################################################
# Service
########################################################################
def test_service_unavailable_page(client):
    response = client.get(reverse("experiments-service-unavailable"))
    assert response.status_code == 200


########################################################################
# Advance participant
########################################################################
@pytest.mark.django_db
def test_anonymous_cant_advance_participant(client):
    session = Recipe(models.Session).make()
    response = client.post(
        reverse(
            "experiments-session-advance-participant", args=(session.pk, "PART-CODE")
        )
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_another_user_cant_advance_participant(client):
    session = Recipe(models.Session).make()
    with login(client):
        response = client.post(
            reverse(
                "experiments-session-advance-participant",
                args=(session.pk, "PART-CODE"),
            )
        )

    assert response.status_code == 404


@pytest.mark.django_db
def test_advance_participant(client, mocker):
    def mock_post(self, endpoint, data={}, json_response=False):
        class ResponseMock:
            def __init__(self):
                self.content = b""

        return ResponseMock()

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._post", mock_post
    )

    with login(client) as user:
        session = Recipe(models.Session, created_by=user).make()
        response = client.post(
            reverse(
                "experiments-session-advance-participant",
                args=(session.pk, "PART-CODE"),
            )
        )

    assert response.status_code == 200


@pytest.mark.django_db
def test_advance_participant_when_otree_not_available(client, mocker):
    def mock_post(self, endpoint, data={}, json_response=False):
        raise otree_exceptions.OTreeNotAvailable

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._post", mock_post
    )

    with login(client) as user:
        session = Recipe(models.Session, created_by=user).make()
        response = client.post(
            reverse(
                "experiments-session-advance-participant",
                args=(session.pk, "PART-CODE"),
            )
        )

    assert response.status_code == 500


########################################################################
# CSV
########################################################################
@pytest.mark.django_db
def test_anonymous_cant_access_csv(client):
    session = Recipe(models.Session).make()
    response = client.get(
        reverse("experiments-session-results-csv", args=(session.pk,))
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_another_user_cant_access_csv(client):
    session = Recipe(models.Session).make()
    with login(client):
        response = client.get(
            reverse("experiments-session-results-csv", args=(session.pk,))
        )

    assert response.status_code == 404


@pytest.mark.django_db
def test_session_csv_can_be_downloaded(client, mocker):
    def mock_get(self, endpoint, data={}, json_response=False):
        class ResponseMock:
            def __init__(self):
                self.content = b"1,2,3"

        return ResponseMock()

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._get", mock_get
    )

    with login(client) as user:
        session = Recipe(models.Session, created_by=user, csv=None).make()
        response = client.get(
            reverse("experiments-session-results-csv", args=(session.pk,))
        )

    session = models.Session.objects.all()[0]
    assert response.status_code == 200
    assert session.csv is not None


@pytest.mark.django_db
def test_session_csv_when_service_not_available(client, mocker):
    def mock_get_unavailable(self, endpoint, data={}, json_response=False):
        raise otree_exceptions.OTreeNotAvailable

    def mock_open(self, encoding):
        return tempfile.TemporaryFile()

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._get",
        mock_get_unavailable,
    )

    mocker.patch("builtins.open", mock_open)

    with login(client) as user:
        session = Recipe(models.Session, created_by=user, csv="sample.csv").make()
        response = client.get(
            reverse("experiments-session-results-csv", args=(session.pk,))
        )

    session = models.Session.objects.all()[0]
    assert response.status_code == 200
    assert session.csv is not None


@pytest.mark.django_db
def test_session_csv_cache(client, mocker):
    def mock_get(self, endpoint, data={}, json_response=False):
        raise otree_exceptions.OTreeNotAvailable

    mocker.patch(
        "ephemer.apps.experiments.otree.connector.OTreeConnector._get", mock_get
    )

    with login(client) as user:
        session = Recipe(models.Session, created_by=user).make()
        response = client.get(
            reverse("experiments-session-results-csv", args=(session.pk,))
        )

    session = models.Session.objects.all()[0]
    assert response.status_code == 404
    assert session.csv is None
