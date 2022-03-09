from django.http import HttpResponse
from django.shortcuts import render as django_render
import pandas as pd
from plotly import graph_objs as go

from .base import compute_bounds, render_graphs, Graphique


def mean_of_selected_columns(data, columns):
    if data.empty:
        return 0
    means_serie = data[columns].mean()
    return means_serie.mean()


def mean_of_selected_columns_with_filter(data, columns, filter_name, filter_value):
    df_filtered = data[data[filter_name] == filter_value]
    return mean_of_selected_columns(df_filtered, columns)


def create_graphique_âge_attribué_cas_1_à_3(data: pd.DataFrame) -> Graphique:

    x = []
    y = []

    column_selection = [
        "player.age_cas1_Entretien",
        "player.age_cas2_Entretien",
        "player.age_cas3_Entretien",
        "player.age_cas1_Photo",
        "player.age_cas2_Photo",
        "player.age_cas3_Photo",
        "player.age_cas1_test_oss",
        "player.age_cas2_test_oss",
        "player.age_cas3_test_oss",
        "player.age_cas1_Etat_civil",
        "player.age_cas2_Etat_civil",
        "player.age_cas3_Etat_civil",
    ]

    data = pd.DataFrame(data, columns=column_selection + ["player.coupable"])
    data = data.dropna()

    # MOYENNE des colonnes sélectionnées AVEC "player.coupable" == "yes"
    x.append(
        "yes",
    )
    y.append(
        mean_of_selected_columns_with_filter(
            data, column_selection, filter_name="player.coupable", filter_value="yes"
        )
    )

    # MOYENNE des colonnes sélectionnées AVEC "player.coupable" == "no"
    x.append(
        "no",
    )
    y.append(
        mean_of_selected_columns_with_filter(
            data, column_selection, filter_name="player.coupable", filter_value="no"
        )
    )

    fig = go.Figure()
    trace = go.Bar(x=x, y=y)
    fig.add_trace(trace)
    fig.update_layout(yaxis_range=compute_bounds(y))
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=["yes", "no"],
            ticktext=["connaissance des conséquences", "ignorance des conséquences"],
        ),
    )
    fig.update_layout(title_text="Âge attribué pour les cas 1 à 3")

    return Graphique(fig)


def create_graphique_certitude_sur_âge_cas_1_à_3(data: pd.DataFrame) -> Graphique:
    x = []
    y = []

    column_selection = [
        "player.confidence_cas1_Entretien",
        "player.confidence_cas2_Entretien",
        "player.confidence_cas3_Entretien",
        "player.confidence_cas1_Photo",
        "player.confidence_cas2_Photo",
        "player.confidence_cas3_Photo",
        "player.confidence_cas1_test_oss",
        "player.confidence_cas2_test_oss",
        "player.confidence_cas3_test_oss",
        "player.confidence_cas1_Etat_civil",
        "player.confidence_cas2_Etat_civil",
        "player.confidence_cas3_Etat_civil",
    ]

    data = pd.DataFrame(data, columns=column_selection + ["player.coupable"])
    data = data.dropna()

    # MOYENNE des colonnes sélectionnées AVEC "player.coupable" == "yes"
    x.append(
        "yes",
    )
    y.append(
        mean_of_selected_columns_with_filter(
            data, column_selection, filter_name="player.coupable", filter_value="yes"
        )
    )

    # MOYENNE des colonnes sélectionnées AVEC "player.coupable" == "no"
    x.append(
        "no",
    )
    y.append(
        mean_of_selected_columns_with_filter(
            data, column_selection, filter_name="player.coupable", filter_value="no"
        )
    )

    fig = go.Figure()
    trace = go.Bar(x=x, y=y)
    fig.add_trace(trace)
    fig.update_layout(yaxis_range=compute_bounds(y))
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=["yes", "no"],
            ticktext=["connaissance des conséquences", "ignorance des conséquences"],
        )
    )
    fig.update_layout(
        title_text="Certitude liée à l’âge attribué pour les cas 1 à 3",
    )
    return Graphique(fig)


def create_trace(data, column_groups, filter_name, filter_value, trace_name):
    data_filtered = data[data[filter_name] == filter_value]
    x = []
    y = []
    for label, columns in column_groups.items():
        x.append(label)
        y.append(mean_of_selected_columns(data_filtered, columns))
    return go.Bar(x=x, y=y, name=trace_name)


def create_graphique_âge_attribué_cas_4_à_5(data: pd.DataFrame) -> Graphique:
    case_4_columns = [
        "player.age_cas4_Entretien",
        "player.age_cas4_Photo",
        "player.age_cas4_test_oss",
        "player.age_cas4_Etat_civil",
    ]
    case_5_columns = [
        "player.age_cas5_Entretien",
        "player.age_cas5_Photo",
        "player.age_cas5_test_oss",
        "player.age_cas5_Etat_civil",
    ]

    column_groups = {
        "Age cas 4": case_4_columns,
        "Age cas 5": case_5_columns,
    }

    data = pd.DataFrame(
        data, columns=case_4_columns + case_5_columns + ["player.coupable"]
    )
    data = data.dropna()

    trace_guilty_yes = create_trace(
        data,
        column_groups=column_groups,
        filter_name="player.coupable",
        filter_value="yes",
        trace_name="cas 4 = 18 ans et cas 5 = 17/19 ans",
    )
    trace_guilty_no = create_trace(
        data,
        column_groups=column_groups,
        filter_name="player.coupable",
        filter_value="no",
        trace_name="cas 4 = 17/19 ans et cas 5 = 18 ans",
    )

    fig = go.Figure()
    fig.add_trace(trace_guilty_yes)
    fig.add_trace(trace_guilty_no)

    y_lower_bound, y_upper_bound = compute_bounds(
        trace_guilty_no.y + trace_guilty_yes.y
    )

    fig.update_layout(yaxis_range=[y_lower_bound, y_upper_bound])
    fig.update_layout(title_text="Âge attribué pour les cas 4 et 5")
    return Graphique(fig)


def create_certitude_âge_cas_4_à_5(data: pd.DataFrame) -> Graphique:

    age_cas_4_columns = [
        "player.age_cas4_Entretien",
        "player.age_cas4_Photo",
        "player.age_cas4_test_oss",
        "player.age_cas4_Etat_civil",
    ]

    age_cas_5_columns = [
        "player.age_cas5_Entretien",
        "player.age_cas5_Photo",
        "player.age_cas5_test_oss",
        "player.age_cas5_Etat_civil",
    ]

    data = pd.DataFrame(
        data, columns=age_cas_4_columns + age_cas_5_columns + ["player.coupable"]
    )
    data = data.dropna()

    column_groups = {
        "Age cas 4": age_cas_4_columns,
        "Age cas 5": age_cas_5_columns,
    }
    trace_coupable_yes = create_trace(
        data,
        column_groups,
        filter_name="player.coupable",
        filter_value="yes",
        trace_name="cas 4 = 18 ans et cas 5 = 17/19 ans",
    )
    trace_coupable_no = create_trace(
        data,
        column_groups,
        filter_name="player.coupable",
        filter_value="no",
        trace_name="cas 4 = 17/19 ans et cas 5 = 18 ans",
    )

    fig = go.Figure()
    fig.add_trace(trace_coupable_yes)
    fig.add_trace(trace_coupable_no)
    fig.update_layout(
        yaxis_range=compute_bounds(trace_coupable_yes.y + trace_coupable_no.y)
    )
    fig.update_layout(
        title_text="Certitude liée à l’âge attribué pour les cas 4 et 5",
    )
    return Graphique(fig)


def create_graphique_âge_attribué_en_fonction_sources_info(
    data: pd.DataFrame,
) -> Graphique:
    x = []
    y = []

    entretien_columns = [
        "player.age_cas1_Entretien",
        "player.age_cas2_Entretien",
        "player.age_cas3_Entretien",
        "player.age_cas4_Entretien",
        "player.age_cas5_Entretien",
    ]
    photo_columns = [
        "player.age_cas1_Photo",
        "player.age_cas2_Photo",
        "player.age_cas3_Photo",
        "player.age_cas4_Photo",
        "player.age_cas5_Photo",
    ]
    test_osseux_columns = [
        "player.age_cas1_test_oss",
        "player.age_cas2_test_oss",
        "player.age_cas3_test_oss",
        "player.age_cas4_test_oss",
        "player.age_cas5_test_oss",
    ]
    etat_civil_columns = [
        "player.age_cas1_Etat_civil",
        "player.age_cas2_Etat_civil",
        "player.age_cas3_Etat_civil",
        "player.age_cas4_Etat_civil",
        "player.age_cas5_Etat_civil",
    ]

    all_columns = (
        entretien_columns + photo_columns + test_osseux_columns + etat_civil_columns
    )

    data = pd.DataFrame(data, columns=all_columns)
    data = data.dropna()

    if not data.empty:
        col_means = data[all_columns].mean()
        x.append("Entretien")
        y.append(col_means[entretien_columns].mean())
        x.append("Photo")
        y.append(col_means[photo_columns].mean())
        x.append("Test osseux")
        y.append(col_means[test_osseux_columns].mean())
        x.append("État civil")
        y.append(col_means[etat_civil_columns].mean())
    else:
        x = ["Entretien", "Photo", "Test osseux", "État civil"]
        y = [0, 0, 0, 0]

    trace = go.Bar(x=x, y=y)
    fig = go.Figure()
    fig.add_trace(trace)
    fig.update_layout(yaxis_range=compute_bounds(y))
    fig.update_layout(
        title_text="Âge donné pour l’ensemble des cas en fonction des différentes sources d’information",
    )
    return Graphique(fig)


def create_graphique_certitude_âge_en_fonction_sources_info(
    data: pd.DataFrame,
) -> Graphique:
    x = []
    y = []

    entretien_columns = [
        "player.confidence_cas1_Entretien",
        "player.confidence_cas2_Entretien",
        "player.confidence_cas3_Entretien",
        "player.confidence_cas4_Entretien",
        "player.confidence_cas5_Entretien",
    ]
    photo_columns = [
        "player.confidence_cas1_Photo",
        "player.confidence_cas2_Photo",
        "player.confidence_cas3_Photo",
        "player.confidence_cas4_Photo",
        "player.confidence_cas5_Photo",
    ]
    test_osseux_columns = [
        "player.confidence_cas1_test_oss",
        "player.confidence_cas2_test_oss",
        "player.confidence_cas3_test_oss",
        "player.confidence_cas4_test_oss",
        "player.confidence_cas5_test_oss",
    ]
    etat_civil_columns = [
        "player.confidence_cas1_Etat_civil",
        "player.confidence_cas2_Etat_civil",
        "player.confidence_cas3_Etat_civil",
        "player.confidence_cas4_Etat_civil",
        "player.confidence_cas5_Etat_civil",
    ]

    all_columns = (
        entretien_columns + photo_columns + test_osseux_columns + etat_civil_columns
    )

    data = pd.DataFrame(data, columns=all_columns)
    data = data.dropna()

    if not data.empty:
        col_means = data[all_columns].mean()
        x.append("Entretien")
        y.append(col_means[entretien_columns].mean())
        x.append("Photo")
        y.append(col_means[photo_columns].mean())
        x.append("Test osseux")
        y.append(col_means[test_osseux_columns].mean())
        x.append("État civil")
        y.append(col_means[etat_civil_columns].mean())
    else:
        x = ["Entretien", "Photo", "Test osseux", "État civil"]
        y = [0, 0, 0, 0]

    trace = go.Bar(x=x, y=y)
    fig = go.Figure()
    fig.add_trace(trace)
    fig.update_layout(yaxis_range=compute_bounds(y))
    fig.update_layout(
        title_text="Certitude liée à l’âge donné pour l’ensemble des cas en fonction des différentes sources d’information",
    )
    return Graphique(fig)


def render(request, session) -> HttpResponse:
    graphs = render_graphs(
        csv_name=session.csv,
        graph_funcs=[
            create_graphique_âge_attribué_cas_1_à_3,
            create_graphique_certitude_sur_âge_cas_1_à_3,
            create_graphique_âge_attribué_cas_4_à_5,
            create_certitude_âge_cas_4_à_5,
            create_graphique_âge_attribué_en_fonction_sources_info,
            create_graphique_certitude_âge_en_fonction_sources_info,
        ],
    )

    return django_render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
