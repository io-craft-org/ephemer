from collections import Counter
from django.http import HttpResponse
from django.shortcuts import render as django_render
import pandas as pd
from plotly import graph_objs as go

from .base import render_graphs, Graphique


def create_graphique_scores_moyens_endogroupe_exogroupe(
    data: pd.DataFrame,
) -> Graphique:
    fig_title = "Scores moyens d’identification et d’appréciation concernant l’endogroupe et l’exogroupe"

    x_labels = (
        "Appréciation de l'endogroupe",
        "Identification à l'endogroupe",
        "Appréciation de l'exogroupe",
        "Identification à l'exogroupe",
    )

    columns = (
        "player.appreciate_picturaux",
        "player.identify_to_picturaux",
        "player.appreciate_experientiels",
        "player.identify_to_experientiels",
    )

    trace = go.Bar(
        x=x_labels,
        y=[data[c].mean() for c in columns],
    )

    fig = go.Figure()
    fig.add_trace(trace)

    fig.update_layout(title_text=fig_title)
    fig.update_yaxes(range=[1, 50])

    return Graphique(fig, title=fig_title)


def _create_graphique_choix_rémunération(serie, choices, title, legend=""):
    def create_label(value):
        return value.replace("_", "-")

    counter = Counter(serie.dropna())

    fig = go.Figure()
    fig.add_trace(trace=go.Bar(x=choices, y=[counter[c] for c in choices]))
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[val for val in choices],
            ticktext=[create_label(val) for val in choices],
        ),
    )
    return Graphique(fig, title=title, legend=legend)


def create_graphique_choix_rémunération_matrice_1(data: pd.DataFrame) -> Graphique:
    legend = (
        "Chaque colonne présente la répartition de rémunération choisie. Le premier chiffre de chaque "
        + "paire correspond à la rémunération choisie pour votre groupe et le second à la rémunération "
        + "choisie pour l’autre groupe. Par exemple le choix de la paire 19-1 implique que vous avez "
        + "décidé de donner une rémunération de 19 pour votre groupe et de 1 pour l’autre groupe."
    )
    choices = [
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
    return _create_graphique_choix_rémunération(
        serie=data["player.matrix1_response"],
        choices=choices,
        title="Distribution des fréquences de choix de rémunération pour la matrice 1",
        legend=legend,
    )


def create_graphique_choix_rémunération_matrice_2(data: pd.DataFrame) -> Graphique:
    legend = (
        "Chaque colonne présente la répartition de rémunération choisie. Le premier chiffre de chaque "
        + "paire correspond à la rémunération choisie pour votre groupe et le second à la rémunération "
        + "choisie pour l’autre groupe. Par exemple le choix de la paire 23-29 implique que vous avez "
        + "décidé de donner une rémunération de 23 pour votre groupe et de 29 pour l’autre groupe."
    )
    choices = [
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
    return _create_graphique_choix_rémunération(
        serie=data["player.matrix2_response"],
        choices=choices,
        title="Distribution des fréquences de choix de rémunération pour la matrice 2",
        legend=legend,
    )


def render(request, session) -> HttpResponse:
    graphs = render_graphs(
        csv_name=session.csv,
        graph_funcs=[
            create_graphique_scores_moyens_endogroupe_exogroupe,
            create_graphique_choix_rémunération_matrice_1,
            create_graphique_choix_rémunération_matrice_2,
        ],
    )

    return django_render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
