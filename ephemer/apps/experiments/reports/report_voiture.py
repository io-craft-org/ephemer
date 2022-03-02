from django.http import HttpResponse
from django.shortcuts import render as django_render
import pandas as pd
from plotly import graph_objs as go

from .base import render_graphs


def create_figures(data):
    # Retire les participants n'ayant pas terminé la session
    data = data[
        data["participant._index_in_pages"] == data["participant._max_page_index"]
    ]

    columns = {
        "player.pop1_nb1": "2_HOMMES",
        "player.pop1_nb2": "3_HOMMES",
        "player.pop1_nb3": "4_HOMMES",
        "player.pop2_nb1": "2_FEMMES",
        "player.pop2_nb2": "3_FEMMES",
        "player.pop2_nb3": "4_FEMMES",
        "player.pop3_nb1": "2_ENFANTS",
        "player.pop3_nb2": "3_ENFANTS",
        "player.pop3_nb3": "4_ENFANTS",
        "player.pop4_nb1": "2_AGES",
        "player.pop4_nb2": "3_AGES",
        "player.pop4_nb3": "4_AGES",
        "player.pop5_nb1": "2_ENCEINTES",
        "player.pop5_nb2": "3_ENCEINTES",
        "player.pop5_nb3": "4_ENCEINTES",
        "player.pop6_nb1": "2_VOLEURS",
        "player.pop6_nb2": "3_VOLEURS",
        "player.pop6_nb3": "4_VOLEURS",
        "player.pop7_nb1": "2_CADRES",
        "player.pop7_nb2": "3_CADRES",
        "player.pop7_nb3": "4_CADRES",
        "player.pop8_leg1": "FEU_ROUGE",
        "player.pop8_leg2": "FEU_VERT",
    }
    selected_columns = list(columns.keys())
    selected_columns.append("player.treatment")
    manip_df = pd.DataFrame(data=data, columns=selected_columns)

    # Convertit le codage '2' pour "sacrifier les occupants" en '0' afin de sommer les valeurs des colonnes.
    manip_df = manip_df.applymap(lambda v: 0 if v == 2 else v)

    manip_df = manip_df.groupby("player.treatment").sum()

    fig = go.Figure()
    fig.add_trace(
        trace=go.Histogram(
            histfunc="sum",
            x=[columns[c] for c in manip_df.columns],
            y=manip_df.sum(axis="index"),
        )
    )
    fig.update_layout(
        barmode="group",
        title_text="Nombre de choix de sacrifier les piétons en fonction des situations présentées",
    )

    fig2 = go.Figure()
    fig2.add_trace(
        trace=go.Histogram(
            histfunc="sum",
            x=[columns[c] for c in manip_df.columns],
            y=manip_df.loc["Decideur"].values,
            name="Décideur",
        )
    )
    fig2.add_trace(
        trace=go.Histogram(
            histfunc="sum",
            x=[columns[c] for c in manip_df.columns],
            y=manip_df.loc["Conducteur"].values,
            name="Conducteur",
        )
    )
    fig2.update_layout(
        barmode="group",
        title_text="Nombre de choix de sacrifier les piétons en fonction des situations présentées selon le rôle joué par les participants",
    )

    return [fig, fig2]


def render(request, session) -> HttpResponse:
    graphs = render_graphs(csv_name=session.csv, figure_funcs=[create_figures])

    return django_render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
