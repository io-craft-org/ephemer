from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from . import forms, models


@login_required
def experiment_list(request):
    experiments = models.Experiment.objects.all()
    return render(
        request,
        template_name="experiments/experiment_list.html",
        context={"experiments": experiments},
    )


@login_required
def experiment_detail(request, experiment_id):
    experiment = get_object_or_404(models.Experiment, pk=experiment_id)
    return render(
        request,
        template_name="experiments/experiment_detail.html",
        context={"experiment": experiment},
    )


@login_required
def experiment_create(request):
    if request.method == "POST":
        form = forms.ExperimentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("experiments-experiment-list"))
    else:
        form = forms.ExperimentForm()

    return render(
        request,
        template_name="experiments/experiment_create.html",
        context={"form": form},
    )


# Sessions
@login_required
def session_list(request):
    sessions = models.Session.objects.all()
    return render(
        request,
        template_name="experiments/session_list.html",
        context={"sessions": sessions},
    )


@login_required
def session_detail(request, session_id):
    session = models.Session.objects.get(pk=session_id)
    return render(
        request,
        template_name="experiments/session_detail.html",
        context={"session": session},
    )
