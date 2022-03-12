from django.http import HttpResponse
from django.shortcuts import render as django_render
import pandas as pd
from plotly import graph_objs as go

from .base import render_graphs, Graphique


def create_graphique(data: pd.DataFrame) -> Graphique:
    return Graphique(figure=go.Figure())


def render(request, session) -> HttpResponse:

    graphs = render_graphs(
        csv_name=session.csv,
        graph_funcs=[create_graphique],
    )

    return django_render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
