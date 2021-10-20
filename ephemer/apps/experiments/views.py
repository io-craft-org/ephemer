from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import (Http404, get_object_or_404, redirect, render,
                              reverse)

from . import forms, models, otree
from .otree import exceptions as otree_exceptions
from .otree.connector import OTreeConnector


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
def session_create(request, experiment_id):
    experiment = get_object_or_404(models.Experiment, pk=experiment_id)

    if request.method == "POST":
        form = forms.SessionCreateForm(request.POST)
        if form.is_valid():
            otree = OTreeConnector(settings.OTREE_API_URL)
            try:
                otree_session = otree.create_session()
            except otree_exceptions.OTreeNotAvailable:
                return redirect("experiments-service-unavailable")

            # FIXME Should handle backend error here

            session = form.save(commit=False)
            session.otree_handler = otree_session.handler
            session.created_by = request.user
            session.experiment = experiment
            session.save()

        return redirect("experiments-session-detail", session_id=session.pk)

    form = forms.SessionCreateForm()

    return render(
        request, template_name="experiments/session_create.html", context={"form": form}
    )


@login_required
def session_list(request):
    sessions = models.Session.objects.filter(created_by=request.user)
    paginator = Paginator(sessions, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        template_name="experiments/session_list.html",
        context={"sessions": page_obj},
    )


@login_required
def session_detail(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    if session.created_by != request.user:
        raise Http404

    return render(
        request,
        template_name="experiments/session_detail.html",
        context={"session": session},
    )


## Service Errors
def service_unavailable(request):
    return render(request, template_name="experiments/service_unavailable.html")
