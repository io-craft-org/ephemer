# encoding: utf-8

"""
Urls for experiments application

"""


from django.urls import path

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
]
