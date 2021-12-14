from django.contrib import admin

from . import models


@admin.register(models.Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(models.ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    pass


class ReportGraphTraceInline(admin.TabularInline):
    model = models.ReportGraphTrace


@admin.register(models.ReportGraph)
class ReportGraphAdmin(admin.ModelAdmin):
    inlines = [ReportGraphTraceInline]


@admin.register(models.ReportDataManipulation)
class ReportDataManipulationAdmin(admin.ModelAdmin):
    pass
