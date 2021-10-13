from django.contrib import admin

from . import models


@admin.register(models.Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ["title"]
