from django.http import HttpResponse
from django.shortcuts import render as django_render
import pandas as pd
from plotly import graph_objs as go
from typing import List

from .base import render_graphs, Graphique


def create_graphiques(data: pd.DataFrame) -> List[Graphique]:
    # Retire les participants n'ayant pas terminé la session
    data = data[
        data["participant._index_in_pages"] == data["participant._max_page_index"]
    ]

    columns = {
        "player.pop1_nb1": "2 hommes",
        "player.pop1_nb2": "3 hommes",
        "player.pop1_nb3": "4 hommes",
        "player.pop2_nb1": "2 femmes",
        "player.pop2_nb2": "3 femmes",
        "player.pop2_nb3": "4 femmes",
        "player.pop3_nb1": "2 enfants",
        "player.pop3_nb2": "3 enfants",
        "player.pop3_nb3": "4 enfants",
        "player.pop4_nb1": "2 pers. âgées",
        "player.pop4_nb2": "3 pers. âgées",
        "player.pop4_nb3": "4 pers. âgées",
        "player.pop5_nb1": "2 femmes enceintes",
        "player.pop5_nb2": "3 femmes enceintes",
        "player.pop5_nb3": "4 femmes enceintes",
        "player.pop6_nb1": "2 voleurs",
        "player.pop6_nb2": "3 voleurs",
        "player.pop6_nb3": "4 voleurs",
        "player.pop7_nb1": "2 cadres",
        "player.pop7_nb2": "3 cadres",
        "player.pop7_nb3": "4 cadres",
        "player.pop8_leg1": "feu rouge",
        "player.pop8_leg2": "feu vert",
    }
    selected_columns = list(columns.keys())
    selected_columns.append("player.treatment")
    manip_df = pd.DataFrame(data=data, columns=selected_columns)

    # Convertit le codage '2' pour "sacrifier les occupants" en '0' afin de sommer les valeurs des colonnes.
    manip_df = manip_df.applymap(lambda v: 0 if v == 2 else v)

    manip_df = manip_df.groupby("player.treatment").sum()

    fig_title = (
        "Nombre de choix de sacrifier les piétons en fonction des situations présentées"
    )
    fig = go.Figure()
    fig.add_trace(
        trace=go.Histogram(
            histfunc="sum",
            x=[columns[c] for c in manip_df.columns],
            y=manip_df.sum(axis="index"),
        )
    )
    fig.update_xaxes(tickangle=45)

    fig2_title = "Nombre de choix de sacrifier les piétons en fonction des situations présentées selon le rôle joué par les participants"
    fig2 = go.Figure()

    if "Decideur" in manip_df.index:
        fig2.add_trace(
            trace=go.Histogram(
                histfunc="sum",
                x=[columns[c] for c in manip_df.columns],
                y=manip_df.loc["Decideur"].values,
                name="Décideur",
            )
        )

    if "Conducteur" in manip_df.index:
        fig2.add_trace(
            trace=go.Histogram(
                histfunc="sum",
                x=[columns[c] for c in manip_df.columns],
                y=manip_df.loc["Conducteur"].values,
                name="Conducteur",
            )
        )

    fig2.update_xaxes(tickangle=45)

    return [
        Graphique(
            fig,
            title=fig_title,
        ),
        Graphique(
            fig2,
            title=fig2_title,
        ),
    ]


def render(request, session) -> HttpResponse:
    graphs = render_graphs(csv_name=session.csv, graph_funcs=[create_graphiques])

    return django_render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
