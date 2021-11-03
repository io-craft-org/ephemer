from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
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


def _get_otree_api_uri():
    return urljoin(settings.OTREE_HOST, settings.OTREE_API_PATH)


@login_required
def session_create(request, experiment_id):
    experiment = get_object_or_404(models.Experiment, pk=experiment_id)

    if request.method == "POST":
        form = forms.SessionCreateForm(request.POST)
        if form.is_valid():
            otree = OTreeConnector(_get_otree_api_uri())
            try:
                otree_session = otree.create_session(experiment.otree_app_name)
            except otree_exceptions.OTreeNotAvailable:
                return redirect("experiments-service-unavailable")

            # FIXME Should handle backend error here

            session = form.save(commit=False)
            session.otree_handler = otree_session.handler
            session.join_in_code = otree_session.join_in_code
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
    sessions = models.Session.objects.filter(created_by=request.user).order_by(
        "-created_on"
    )
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

    otree_session = None

    otree = OTreeConnector(_get_otree_api_uri())
    try:
        otree_session = otree.get_session(session.otree_handler)
    except otree_exceptions.OTreeNotAvailable:
        pass

    return render(
        request,
        template_name="experiments/session_detail.html",
        context={"session": session, "otree_session": otree_session},
    )


@login_required
def session_participants_state_json(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)
    if session.created_by != request.user:
        raise Http404

    otree = OTreeConnector(_get_otree_api_uri())
    try:
        session_participants = otree.get_session_participants(session.otree_handler)
    except otree_exceptions.OTreeNotAvailable:
        pass

    state_json = [participant.to_dict() for participant in session_participants]

    print(state_json)

    return JsonResponse(state_json, safe=False)


def session_join(request, session_id):
    session = get_object_or_404(models.Session, pk=session_id)

    form = forms.SessionJoinForm()

    return render(
        request,
        template_name="experiments/session_join.html",
        context={"session": session, "form": form},
    )


def participant_join_session(request):
    error = None
    if request.method == "POST":
        form = forms.ParticipantJoinSessionForm(request.POST)
        if form.is_valid():
            try:
                session = models.Session.objects.get(
                    pin_code=form.cleaned_data["pin_code"]
                )
            except models.Session.DoesNotExist:
                error = "Le PIN code saisi ne correspond pas à aucune session en cours."
            else:
                return redirect(
                    urljoin(settings.OTREE_HOST, f"/join/{session.join_in_code}")
                )

    form = forms.ParticipantJoinSessionForm()

    return render(
        request,
        template_name="experiments/participant_join_session.html",
        context={"form": form, "error": error},
    )


## Service Errors
def service_unavailable(request):
    return render(request, template_name="experiments/service_unavailable.html")
