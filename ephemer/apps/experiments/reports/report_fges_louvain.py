import re

from django.http import HttpResponse
from django.shortcuts import render as django_render
import pandas as pd
from plotly import graph_objs as go

from .base import compute_bounds, render_graphs, Graphique

label_pattern = re.compile("([0-9]+)_([0-9]+)")


def _create_graphique_choix_rémunération(serie, category_order, title, legend=""):
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
    return Graphique(fig, legend)


def create_graphique_choix_rémunération_matrice_1(data: pd.DataFrame) -> Graphique:
    legend = (
        "Chaque colonne présente la répartition de rémunération choisie. Le premier chiffre de chaque "
        + "paire correspond à la rémunération choisie pour votre groupe et le second à la rémunération "
        + "choisie pour l’autre groupe. Par exemple le choix de la paire 19-1 implique que vous avez "
        + "décidé de donner une rémunération de 19 pour votre groupe et de 1 pour l’autre groupe."
    )
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
    return _create_graphique_choix_rémunération(
        serie=data["player.matrix1_response"],
        category_order=category_order_array,
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
    return _create_graphique_choix_rémunération(
        serie=data["player.matrix2_response"],
        category_order=category_order_array,
        title="Distribution des fréquences de choix de rémunération pour la matrice 2",
        legend=legend,
    )


def create_graphique_identification(data: pd.DataFrame) -> Graphique:
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

    return Graphique(fig)


def create_graphique_appréciation(data: pd.DataFrame) -> Graphique:
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

    return Graphique(fig)


def create_graphique_scores_moyens_généraux(data: pd.DataFrame) -> Graphique:
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

    return Graphique(fig)


def render(request, session) -> HttpResponse:

    graphs = render_graphs(
        csv_name=session.csv,
        graph_funcs=[
            create_graphique_choix_rémunération_matrice_1,
            create_graphique_choix_rémunération_matrice_2,
            create_graphique_identification,
            create_graphique_appréciation,
            create_graphique_scores_moyens_généraux,
        ],
    )

    return django_render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
