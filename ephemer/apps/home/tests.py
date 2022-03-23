import django.core.mail
import pytest
from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from ephemer.utils import login


####
# sending message to team
####


def test_user_can_access_contact_form(client):

    url = reverse("home-contact") + "?next=/"
    response = client.get(url)

    assert b"<form " in response.content


@pytest.mark.django_db
@override_settings(TEAM_EMAILS=("x@y.org",))
def test_non_logged_user_can_send_message_to_team(mocker, client):

    mocker.patch("django.core.mail.send_mail")

    data = {
        "firstname": "Bob",
        "lastname": "Joe",
        "email": "bob@bob.com",
        "subject": "a subject",
        "content": "some content",
    }
    url = reverse("home-contact") + "?next=/"
    response = client.post(url, data=data)

    content = "{0}\n\nfrom: {1} {2} <{3}>".format(
        data["content"], data["firstname"], data["lastname"], data["email"]
    )

    django.core.mail.send_mail.assert_called_once_with(
        subject=data["subject"],
        message=content,
        from_email=settings.EMAIL_FROM,
        recipient_list=settings.TEAM_EMAILS,
        fail_silently=True,
    )

    assertRedirects(response, "/")


@pytest.mark.django_db
@override_settings(TEAM_EMAILS=("x@y.org",))
def test_logged_user_can_send_message_to_team(mocker, client):

    mocker.patch("django.core.mail.send_mail")

    data = {
        "firstname": "Bob",
        "lastname": "Joe",
        "email": "bob@bob.com",
        "subject": "a subject",
        "content": "some content",
    }
    url = reverse("home-contact") + "?next=/"
    with login(client, is_staff=False):
        response = client.post(url, data=data)

    content = "{0}\n\nfrom: {1} {2} <{3}>".format(
        data["content"], data["firstname"], data["lastname"], data["email"]
    )

    django.core.mail.send_mail.assert_called_once_with(
        subject=data["subject"],
        message=content,
        from_email=settings.EMAIL_FROM,
        recipient_list=settings.TEAM_EMAILS,
        fail_silently=True,
    )

    assertRedirects(response, "/")
