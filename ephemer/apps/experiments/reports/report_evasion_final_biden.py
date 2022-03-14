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


def create_graphique_taux_imposition_décidés(data: pd.DataFrame) -> Graphique:
    fig_title = "Taux d’imposition décidé par les joueurs A pour chaque round"

    nb_of_groups = data["player.NUMBER_OF_GROUPS"][0]
    round_numbers_axis = list(range(1, max(data["subsession.round_number"]) + 1))

    data = data[data["player.ROLE"] == "A"]
    data = data[
        [
            "player.A_TX_IMPOT",
            "player.B_CHOOSE_GROUPE",
            "player.GROUP_NAME_PARTICIPANT",
            "subsession.round_number",
        ]
    ]
    data = data.sort_values(by="subsession.round_number")

    fig = go.Figure()

    vertical_bar = go.Scatter(
        x=[3, 3], y=[-5, 55], line_color="black", mode="lines", showlegend=False
    )
    fig.add_trace(vertical_bar)

    for group_index in range(1, nb_of_groups + 1):
        group_data = data[data["player.B_CHOOSE_GROUPE"] == group_index]
        group_name = pick_value_if_unique(group_data["player.GROUP_NAME_PARTICIPANT"])
        color = COLORS_MAP[group_name]
        trace = go.Scatter(
            x=round_numbers_axis,
            y=group_data["player.A_TX_IMPOT"],
            marker={"color": color, "line": {"color": "black", "width": 1}},
            line={"dash": "dash"},
            name="groupe " + group_name,
        )
        fig.add_trace(trace)

    medians = data.groupby("subsession.round_number").median()["player.A_TX_IMPOT"]
    fig.add_trace(
        go.Scatter(
            x=round_numbers_axis,
            y=medians,
            line={"width": 3, "color": "black"},
            name="médiane",
            mode="lines",
        )
    )

    margin = 5
    fig.update_layout(title_text=fig_title)
    fig.update_yaxes(range=[0 - margin, 50 + margin], title_text="taux d'imposition %")
    fig.update_xaxes(tick0=1, dtick=1, title_text="rounds")

    return Graphique(figure=fig)


def render(request, session) -> HttpResponse:

    graphs = render_graphs(
        csv_name=session.csv,
        graph_funcs=[create_graphique_taux_imposition_décidés],
    )

    return django_render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
