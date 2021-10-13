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
        r"sessions/<int:id>/",
        views.session_detail,
        name="experiments-session-detail",
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
]
