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
        r"xp/",
        views.experiment_list,
        name="experiments-experiment-list",
    ),
]
