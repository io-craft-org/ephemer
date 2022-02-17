import base64
from typing import List

from django.http import HttpResponse
import pandas as pd
from plotly import graph_objs as go

from .layout import BASE_LAYOUT, compute_bounds


def create_figures_choix_rémunération(data: pd.DataFrame) -> List[go.Figure]:

    choix_1_serie = data["player.matrix1_response"]
    fig1 = go.Figure()
    fig1.add_trace(
        trace=go.Histogram(
            histfunc="count",
            x=choix_1_serie,
        )
    )
    fig1.update_layout(
        title_text="Distribution des fréquences de choix de rémunération pour la matrice 1",
    )

    choix_2_serie = data["player.matrix2_response"]
    fig2 = go.Figure()
    fig2.add_trace(
        trace=go.Histogram(
            histfunc="count",
            x=choix_2_serie,
        )
    )
    fig2.update_layout(
        title_text="Distribution des fréquences de choix de rémunération pour la matrice 2",
    )

    return [fig1, fig2]


def create_figure_identification(data: pd.DataFrame) -> go.Figure:
    fig_title = "Scores moyens d’identification en fonction du groupe d’appartenance"

    x_labels = (
        'Identification au groupe des "Focalisés"',
        'Identification au groupe des "Holistiques"',
    )

    df1 = data[data["player.perso"] == "focal"]
    trace1 = go.Bar(
        x=x_labels,
        y=(
            df1["player.identify_to_focal"].mean(),
            df1["player.identify_to_holi"].mean(),
        ),
        name='Groupe "Focalisés"',
    )

    df2 = data[data["player.perso"] == "holi"]
    trace2 = go.Bar(
        x=x_labels,
        y=(
            df2["player.identify_to_focal"].mean(),
            df2["player.identify_to_holi"].mean(),
        ),
        name='Groupe "Holistiques"',
    )

    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)

    fig.update_layout(title_text=fig_title)

    return fig


def create_figure_appréciation(data: pd.DataFrame) -> go.Figure:
    fig_title = "Scores moyens d’appréciation en fonction du groupe d’appartenance"

    x_labels = (
        'Appréciation du groupe des "Focalisés"',
        'Appréciation du groupe des "Holistiques"',
    )

    df1 = data[data["player.perso"] == "focal"]
    trace1 = go.Bar(
        x=x_labels,
        y=(
            df1["player.appreciate_focal"].mean(),
            df1["player.appreciate_holi"].mean(),
        ),
        name='Groupe "Focalisés"',
    )

    df2 = data[data["player.perso"] == "holi"]
    trace2 = go.Bar(
        x=x_labels,
        y=(
            df2["player.appreciate_focal"].mean(),
            df2["player.appreciate_holi"].mean(),
        ),
        name='Groupe "Holistiques"',
    )

    fig = go.Figure()
    fig.add_trace(trace1)
    fig.add_trace(trace2)

    fig.update_layout(title_text=fig_title)

    return fig


def create_figure_scores_moyens_généraux(data: pd.DataFrame) -> go.Figure:
    fig_title = "Scores moyens généraux observés suite au feedback, en fonction du groupe d’appartenance"

    entativité_columns = [
        "player.nous_groupe",
        "player.nous_similaires",
        "player.vision_commune",
    ]
    efficacité_groupale_columns = [
        "player.travail_ensemble",
        "player.mots_nouveaux",
        "player.amelioration",
    ]
    identification_columns = [
        "player.appreciate_self",
        "player.identify_to_self",
    ]
    cohésion_columns = [
        "player.appartenance",
        "player.heureux",
        "player.faisant_partie",
        "player.meilleurs",
        "player.sentiment_membre",
        "player.satisfait",
    ]
    fig_columns = (
        entativité_columns
        + efficacité_groupale_columns
        + identification_columns
        + cohésion_columns
    )

    fig = go.Figure()
    all_y_values = []

    for role, trace_name in [
        ("focal", 'Groupe "Focalisés"'),
        ("holi", 'Groupe "Holistiques"'),
    ]:
        x = []
        y = []
        df = data[data["player.perso"] == role]
        df = pd.DataFrame(data=df, columns=fig_columns)
        means_serie = df.mean()

        for label, columns in [
            ("Entativité", entativité_columns),
            ("Efficacité groupale", efficacité_groupale_columns),
            ("Identification", identification_columns),
            ("Cohésion", cohésion_columns),
        ]:
            x.append(label)
            y.append(sum([means_serie[c] for c in columns]) / len(columns))

        trace = go.Bar(x=x, y=y, name=trace_name)
        fig.add_trace(trace)
        all_y_values.extend(y)

    fig.update_layout(title_text=fig_title)
    fig.update_layout(yaxis_range=compute_bounds(all_y_values))
    return fig


def render(request, session) -> HttpResponse:
    from django.shortcuts import render

    data = pd.read_csv(session.csv)

    data = data[
        data["participant._index_in_pages"] >= data["participant._max_page_index"]
    ]

    figures = []
    figures.extend(create_figures_choix_rémunération(data))
    figures.append(create_figure_identification(data))
    figures.append(create_figure_appréciation(data))
    figures.append(create_figure_scores_moyens_généraux(data))

    graphs = []
    for figure in figures:
        figure.update_layout(**BASE_LAYOUT)
        graphs.append(
            base64.b64encode(figure.to_image(format="png", width=1000)).decode("utf-8")
        )

    return render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
