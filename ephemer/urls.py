"""ephemer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from experiments import views as experiments_views
from home import views as home_views
from magicauth.urls import urlpatterns as magicauth_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_views.Home.as_view(), name="home"),
    path(
        "experiments/",
        experiments_views.experiment_list,
        name="experiments-experiment-list",
    ),
    path(
        "experiments-cbv/",
        experiments_views.ExperimentList2.as_view(),
        name="experiments-experiment-list-cbv",
    ),
    path(
        "experiments/<int:experiment_id>/",
        experiments_views.experiment_detail,
        name="experiments-experiment-detail",
    ),
    path(
        "experiments-cbv/<int:experiment_id>/",
        experiments_views.ExperimentDetail.as_view(),
        name="experiments-experiment-detail-cbv",
    ),
    path(
        "experiments/new/",
        experiments_views.experiment_create,
        name="experiments-experiment-create",
    ),
    path(
        "experiments-cbv/new/",
        experiments_views.ExperimentCreate.as_view(),
        name="experiments-experiment-create-cbv",
    ),
    path("__debug__/", include(debug_toolbar.urls)),
]

urlpatterns.extend(magicauth_urls)
