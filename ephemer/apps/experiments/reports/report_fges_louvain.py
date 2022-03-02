import re

from django.http import HttpResponse
from django.shortcuts import render as django_render
import pandas as pd
from plotly import graph_objs as go

from .base import compute_bounds, render_graphs

label_pattern = re.compile("([0-9]+)_([0-9]+)")


def _create_figure_choix_rémunération(serie, category_order, title):
    def create_label(value):
        result = label_pattern.search(value)
        return f"{result.groups()[0]}-{result.groups()[1]}"

    fig = go.Figure()
    fig.add_trace(
        trace=go.Histogram(
            histfunc="count",
            x=serie,
        )
    )
    fig.update_xaxes(categoryorder="array", categoryarray=category_order)
    fig.update_layout(
        title_text=title,
        xaxis=dict(
            tickmode="array",
            tickvals=[val for val in category_order],
            ticktext=[create_label(val) for val in category_order],
        ),
    )
    return fig


def create_figure_choix_rémunération_matrice_1(data):
    category_order_array = [
        "7_25",
        "8_23",
        "9_21",
        "10_19",
        "11_17",
        "12_15",
        "13_13",
        "14_11",
        "15_9",
        "16_7",
        "17_5",
        "18_3",
        "19_1",
    ]
    return _create_figure_choix_rémunération(
        serie=data["player.matrix1_response"],
        category_order=category_order_array,
        title="Distribution des fréquences de choix de rémunération pour la matrice 1",
    )


def create_figure_choix_rémunération_matrice_2(data):
    category_order_array = [
        "11_5",
        "12_7",
        "13_9",
        "14_11",
        "15_13",
        "16_15",
        "17_17",
        "18_19",
        "19_21",
        "20_23",
        "21_25",
        "22_27",
        "23_29",
    ]
    return _create_figure_choix_rémunération(
        serie=data["player.matrix2_response"],
        category_order=category_order_array,
        title="Distribution des fréquences de choix de rémunération pour la matrice 2",
    )


def create_figure_identification(data: pd.DataFrame):
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


def create_figure_appréciation(data: pd.DataFrame):
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


def create_figure_scores_moyens_généraux(data: pd.DataFrame):
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

    graphs = render_graphs(
        csv_name=session.csv,
        figure_funcs=[
            create_figure_choix_rémunération_matrice_1,
            create_figure_choix_rémunération_matrice_2,
            create_figure_identification,
            create_figure_appréciation,
            create_figure_scores_moyens_généraux,
        ],
    )

    return django_render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
