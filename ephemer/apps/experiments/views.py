import base64
import os
from urllib.parse import urljoin

import pandas as pd
import plotly.graph_objects as go
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import (Http404, get_object_or_404, redirect, render,
                              reverse)

from . import forms, models
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
            # In case we asked more slots than possible
            participant_count = form.cleaned_data.get("participant_count")
            if participant_count > experiment.participant_count:
                form.cleaned_data["participant_count"] = experiment.participant_count

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

    form = forms.SessionCreateForm(
        initial={"participant_count": experiment.participant_count}
    )

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
def session_participants_state_json(request, session_id: int):
    session = get_object_or_404(models.Session, pk=session_id)
    if session.created_by != request.user:
        raise Http404

    otree = OTreeConnector(_get_otree_api_uri())
    try:
        session_participants = otree.get_session_participants(session.otree_handler)
    except otree_exceptions.OTreeNotAvailable:
        session_participants = []

    state_json = [participant.to_dict() for participant in session_participants]

    return JsonResponse(state_json, safe=False)


@login_required
def session_advance_participant(request, session_id: int, participant_code: str):
    """Advance a participant to the next step"""
    # XXX We might have a security issue here if the caller supply a session_id
    # she's owner and a participant code from another session
    session = get_object_or_404(models.Session, pk=session_id)
    if session.created_by != request.user:
        raise Http404

    otree = OTreeConnector(_get_otree_api_uri())
    try:
        response = otree.session_advance_participant(participant_code)
    except otree_exceptions.OTreeNotAvailable:
        return HttpResponse(status=500)

    return HttpResponse(status=200)


@login_required
def session_results_as_csv(request, session_id: int):
    """Get raw results of a sesssion, as CSV"""
    session = get_object_or_404(models.Session, pk=session_id)
    if session.created_by != request.user:
        raise Http404

    otree = OTreeConnector(_get_otree_api_uri())
    try:
        response = otree.get_session_results_as_csv(session.otree_handler)
    except otree_exceptions.OTreeNotAvailable:
        response = None

    base_dir = models.get_csv_path()
    os.makedirs(base_dir, exist_ok=True)
    filepath = os.path.join(base_dir, f"{session.id}.csv")

    if response:
        with open(filepath, "wb") as f:
            f.write(response.content)

        session.csv = filepath
        session.save()
    else:
        if not session.csv:
            return HttpResponse(status=404)

    return FileResponse(open(session.csv, "rb"))


@login_required
def session_results(request, session_id: int):
    """Get results of a sesssion, output as HTML"""
    session = get_object_or_404(models.Session, pk=session_id)
    if session.created_by != request.user:
        raise Http404

    otree = OTreeConnector(_get_otree_api_uri())
    try:
        response = otree.get_session_results_as_csv(session.otree_handler)
    except otree_exceptions.OTreeNotAvailable:
        response = None

    base_dir = models.get_csv_path()
    os.makedirs(base_dir, exist_ok=True)
    filepath = os.path.join(base_dir, f"{session.id}.csv")

    if response:
        with open(filepath, "wb") as f:
            f.write(response.content)

        session.csv = filepath
        session.save()
    else:
        if not session.csv:
            return HttpResponse(status=404)

    # Compute graphs
    graphs = []

    df = pd.read_csv(session.csv)

    report_tmpl = session.experiment.report_template

    if report_tmpl:
        for data_manipulation in report_tmpl.data_manipulations.order_by(
            "position"
        ).all():
            manip_df = pd.DataFrame(df, columns=data_manipulation.columns)
            df[data_manipulation.data_name] = manip_df.agg(
                func=data_manipulation.func, axis="columns"
            )

        for graph in report_tmpl.graphs.order_by("position").all():
            fig = go.Figure()
            for trace in graph.traces.all():
                if trace.y:
                    y = df[trace.y]
                else:
                    y = None

                fig.add_trace(
                    go.Histogram(
                        x=df[trace.x],
                        y=y,
                        # histnorm="density",
                        histfunc=trace.func or None,
                        name=trace.name,
                    )
                )

            if graph.x_tick_labels:
                fig.update_layout(
                    xaxis=dict(
                        tickmode="array",
                        tickvals=[val for val in graph.x_tick_labels.keys()],
                        ticktext=[text for text in graph.x_tick_labels.values()],
                    )
                )

            fig.update_layout(
                barmode="group",
                title_text=graph.title,
            )

            graphs.append(
                base64.b64encode(fig.to_image(format="png", width=1000)).decode("utf-8")
            )

    return render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )


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
                error = "Le PIN code saisi ne correspond à aucune session en cours."
            else:
                return redirect(
                    urljoin(settings.OTREE_HOST, f"/join/{session.join_in_code}")
                )

    form = forms.ParticipantJoinSessionForm()

    return render(
        request,
        template_name="experiments/participant_join_session.html",
        context={
            "form": form,
            "error": error,
            "pin_code_length": models.PIN_CODE_LENGTH,
        },
    )


## Service Errors
def service_unavailable(request):
    return render(request, template_name="experiments/service_unavailable.html")
