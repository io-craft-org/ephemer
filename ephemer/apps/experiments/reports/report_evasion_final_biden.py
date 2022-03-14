from django.http import HttpResponse
from django.shortcuts import render as django_render
import pandas as pd
from plotly import graph_objs as go

from .base import render_graphs, Graphique


COLORS_MAP = {
    "bleu": "blue",
    "jaune": "yellow",
    "orange": "orange",
    "rouge": "red",
    "vert": "green",
    "noir": "black",
    "blanc": "white",
}


def are_values_identical(iterable):
    first = True
    previous = None
    for value in iterable:
        if first:
            previous = value
            first = False
        else:
            if previous != value:
                return False
    return True


def pick_value_if_unique(serie: pd.Series):
    assert are_values_identical(serie) is True
    return serie.iloc[0]


def create_graphique_joueur_A(
    data: pd.DataFrame, column_name, yaxis_title, yaxis_range, fig_title
) -> Graphique:
    nb_of_groups = data["player.NUMBER_OF_GROUPS"][0]
    round_numbers_axis = list(range(1, max(data["subsession.round_number"]) + 1))

    data = data[data["player.ROLE"] == "A"]
    data = data[
        [
            column_name,
            "player.B_CHOOSE_GROUPE",
            "player.GROUP_NAME_PARTICIPANT",
            "subsession.round_number",
        ]
    ]
    data = data.sort_values(by="subsession.round_number")

    fig = go.Figure()

    margin = 5
    y_min = yaxis_range[0] - margin
    y_max = yaxis_range[1] + margin
    vertical_bar = go.Scatter(
        x=[3, 3], y=[y_min, y_max], line_color="black", mode="lines", showlegend=False
    )
    fig.add_trace(vertical_bar)

    for group_index in range(1, nb_of_groups + 1):
        group_data = data[data["player.B_CHOOSE_GROUPE"] == group_index]
        group_name = pick_value_if_unique(group_data["player.GROUP_NAME_PARTICIPANT"])
        color = COLORS_MAP[group_name]
        trace = go.Scatter(
            x=round_numbers_axis,
            y=group_data[column_name],
            marker={"color": color, "line": {"color": "black", "width": 1}},
            line={"dash": "dash"},
            name="groupe " + group_name,
        )
        fig.add_trace(trace)

    medians = data.groupby("subsession.round_number").median()[column_name]
    fig.add_trace(
        go.Scatter(
            x=round_numbers_axis,
            y=medians,
            line={"width": 3, "color": "black"},
            name="médiane",
            mode="lines",
        )
    )

    fig.update_layout(title_text=fig_title)
    fig.update_yaxes(range=[y_min, y_max], title_text=yaxis_title)
    fig.update_xaxes(tick0=1, dtick=1, title_text="rounds")

    return Graphique(figure=fig)


def create_graphique_taux_imposition_décidés(data: pd.DataFrame) -> Graphique:
    return create_graphique_joueur_A(
        data,
        column_name="player.A_TX_IMPOT",
        yaxis_title="taux d'imposition %",
        yaxis_range=[0, 50],
        fig_title="Taux d’imposition décidé par les joueurs A pour chaque round",
    )


def create_graphique_taux_redistribution_décidés(data: pd.DataFrame) -> Graphique:
    return create_graphique_joueur_A(
        data,
        column_name="player.A_TX_REDISTRIB",
        yaxis_title="taux de redistribution %",
        yaxis_range=[0, 100],
        fig_title="Taux de redistribution décidé par les joueurs A pour chaque round",
    )


def create_graphique_proportion_fraude_joueurs_B_et_C(data: pd.DataFrame) -> Graphique:
    fig_title = "Proportion de joueurs B et C ayant fraudé pour chaque round"

    nb_of_groups = data["player.NUMBER_OF_GROUPS"][0]
    round_numbers_axis = list(range(1, max(data["subsession.round_number"]) + 1))
    yaxis_range = [0, 100]

    # Retire les joueurs A
    data = data[data["player.ROLE"] != "A"]

    # Sélectionne uniquement les colonnes nécessaires
    data = data[
        [
            "player.ROLE",
            "player.FRAUDE",
            "player.GROUP_NAME_PARTICIPANT",
            "subsession.round_number",
            "group.NUMB_PLAYER_PER_GROUP",
            "player.NUMBER_OF_GROUPS",
            "player.B_CHOOSE_GROUPE",
        ]
    ]

    # On s'assure que les lignes sont bien triées par round number
    data = data.sort_values(by="subsession.round_number")

    fig = go.Figure()

    # On ajoute la barre verticale qui indique la phase 2 au round 6
    margin = 5
    y_min = yaxis_range[0] - margin
    y_max = yaxis_range[1] + margin
    vertical_bar = go.Scatter(
        x=[3, 3], y=[y_min, y_max], line_color="black", mode="lines", showlegend=False
    )
    fig.add_trace(vertical_bar)

    # Ajout de la proportion de fraude pour chaque groupe
    proportions_fraude = []
    for group_index in range(1, nb_of_groups + 1):
        group_data = data[data["player.B_CHOOSE_GROUPE"] == group_index]
        group_name = pick_value_if_unique(group_data["player.GROUP_NAME_PARTICIPANT"])
        color = COLORS_MAP[group_name]
        group_data = group_data.assign(
            proportion_fraude=group_data["player.FRAUDE"]
            * 100
            / (group_data["group.NUMB_PLAYER_PER_GROUP"] - 1)
        )
        y = group_data.groupby(by="subsession.round_number").sum()["proportion_fraude"]
        proportions_fraude.append(y)
        trace = go.Scatter(
            x=round_numbers_axis,
            y=y,
            marker={"color": color, "line": {"color": "black", "width": 1}},
            line={"dash": "dash"},
            name="% fraude groupe " + group_name,
        )
        fig.add_trace(trace)

    # Avec les proportions de fraude dans chaque groupe ajout de la proportion générale
    fig.add_trace(
        go.Scatter(
            x=round_numbers_axis,
            y=[sum(t) / len(proportions_fraude) for t in zip(*proportions_fraude)],
            line={"color": "black"},
            mode="lines",
            name="% fraude",
        )
    )

    fig.update_layout(title_text=fig_title)
    fig.update_yaxes(title_text="Fréquence de fraude %")
    fig.update_xaxes(tick0=1, dtick=1, title_text="rounds")

    return Graphique(figure=fig)


def render(request, session) -> HttpResponse:

    graphs = render_graphs(
        csv_name=session.csv,
        graph_funcs=[
            create_graphique_taux_imposition_décidés,
            create_graphique_taux_redistribution_décidés,
            create_graphique_proportion_fraude_joueurs_B_et_C,
        ],
    )

    return django_render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )