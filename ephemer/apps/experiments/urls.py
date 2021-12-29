# encoding: utf-8

"""
Urls for experiments application

"""

from django.conf.urls import url
from django.urls import include, path

from . import views

urlpatterns = [
    path(
        r"sessions/",
        views.session_list,
        name="experiments-session-list",
    ),
    path(
        r"sessions/<int:session_id>/",
        views.session_detail,
        name="experiments-session-detail",
    ),
    path(
        r"sessions/<int:session_id>/delete",
        views.session_delete,
        name="experiments-session-delete",
    ),
    path(
        r"sessions/<int:session_id>/state.json",
        views.session_participants_state_json,
        name="experiments-session-participants-state-json",
    ),
    path(
        r"sessions/<int:session_id>/advance/<str:participant_code>",
        views.session_advance_participant,
        name="experiments-session-advance-participant",
    ),
    path(
        r"sessions/<int:session_id>/results",
        views.session_results,
        name="experiments-session-results",
    ),
    path(
        r"sessions/<int:session_id>/export.csv",
        views.session_results_as_csv,
        name="experiments-session-results-csv",
    ),
    path(
        r"sessions/<int:session_id>/join",
        views.session_join,
        name="experiments-session-join",
    ),
    path(
        r"sessions/service-unavailable",
        views.service_unavailable,
        name="experiments-service-unavailable",
    ),
    path(
        r"xp/",
        views.experiment_list,
        name="experiments-experiment-list",
    ),
    path(
        r"xp/<int:experiment_id>",
        views.experiment_detail,
        name="experiments-experiment-detail",
    ),
    path(
        r"xp/<int:experiment_id>/create",
        views.session_create,
        name="experiments-session-create",
    ),
    path(
        r"join-session",
        views.participant_join_session,
        name="experiments-participant-join-session",
    ),
    url(r"^markdownx/", include("markdownx.urls")),
]
