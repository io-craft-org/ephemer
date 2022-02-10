import base64
from math import ceil
from numbers import Number
from typing import Optional

from django.http import HttpResponse

import pandas as pd
from plotly import graph_objs as go


BASE_LAYOUT = {"font_size": 20, "barmode": "group", "bargap": 0.6}


def compute_bounds(
    values,
    zero_lower_bound: Optional[bool] = None,
    minimal_range: Optional[Number] = None,
    precision: Number = 0.1,
):
    if zero_lower_bound:
        lower_bound = 0
        max_value = max(values)
        upper_bound = max_value * 1.2
    else:
        min_value = min(values)
        max_value = max(values)
        diff = max_value - min_value
        upper_bound = min_value + diff * (1 + 15 / 55)
        lower_bound = min_value - diff * 30 / 55
    if minimal_range:
        upper_bound = max(upper_bound, lower_bound + minimal_range)

    def round_at_precision(n):
        return ceil(n / precision) * precision

    return round_at_precision(lower_bound), round_at_precision(upper_bound)


def compute_mean_on_columns_with_filter(data, columns, filter_name, filter_value):
    if data.empty:
        return 0
    df_grouped = data.groupby(filter_name).mean()
    df_filtered = pd.DataFrame(data=df_grouped, columns=columns)
    df_transposed = df_filtered.transpose()
    return df_transposed[filter_value].mean()


def create_age_fig_cases_1_to_3(data: pd.DataFrame) -> go.Figure:

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
        compute_mean_on_columns_with_filter(
            data, column_selection, filter_name="player.coupable", filter_value="yes"
        )
    )

    # MOYENNE des colonnes sélectionnées AVEC "player.coupable" == "no"
    x.append(
        "no",
    )
    y.append(
        compute_mean_on_columns_with_filter(
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
    fig.update_layout(**BASE_LAYOUT)
    return fig


def create_confidence_fig_cases_1_to_3(data):
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
        compute_mean_on_columns_with_filter(
            data, column_selection, filter_name="player.coupable", filter_value="yes"
        )
    )

    # MOYENNE des colonnes sélectionnées AVEC "player.coupable" == "no"
    x.append(
        "no",
    )
    y.append(
        compute_mean_on_columns_with_filter(
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
    fig.update_layout(**BASE_LAYOUT)
    return fig


def create_age_fig_cases_4_and_5(data: pd.DataFrame) -> go.Figure:
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

    data = pd.DataFrame(
        data, columns=case_4_columns + case_5_columns + ["player.coupable"]
    )
    data = data.dropna()

    def create_trace(data, filter, name):
        df_grouped = data.groupby("player.coupable").mean()

        x = []
        y = []

        for case_label, case_columns in {
            "Age cas 4": case_4_columns,
            "Age cas 5": case_5_columns,
        }.items():
            x.append(case_label)

            if not data.empty:
                df_filtered = pd.DataFrame(data=df_grouped, columns=case_columns)
                df_transposed = df_filtered.transpose()
                serie = df_transposed[filter]
                y.append(serie.mean())
            else:
                y.append(0)

        return go.Bar(x=x, y=y, name=name)

    trace_guilty_yes = create_trace(
        data, filter="yes", name="cas 4 = 18 ans et cas 5 = 17/19 ans"
    )
    trace_guilty_no = create_trace(
        data, filter="no", name="cas 4 = 17/19 ans et cas 5 = 18 ans"
    )

    fig = go.Figure()
    fig.add_trace(trace_guilty_yes)
    fig.add_trace(trace_guilty_no)

    y_lower_bound, y_upper_bound = compute_bounds(
        trace_guilty_no.y + trace_guilty_yes.y
    )

    fig.update_layout(yaxis_range=[y_lower_bound, y_upper_bound])
    fig.update_layout(title_text="Âge attribué pour les cas 4 et 5")
    fig.update_layout(**BASE_LAYOUT)
    return fig


def create_confidence_fig_cases_4_and_5(data: pd.DataFrame) -> go.Figure:

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

    def create_trace(data, column_groups, filter, name):
        x = []
        y = []
        for label, columns in column_groups.items():
            x.append(label)
            if not data.empty:
                df = pd.DataFrame(data, columns=columns)
                df = df.transpose()
                serie = df[filter]
                y.append(serie.mean())
            else:
                y.append(0)
        return go.Bar(x=x, y=y, name=name)

    data = data.groupby("player.coupable").mean()

    column_groups = {
        "Age cas 4": age_cas_4_columns,
        "Age cas 5": age_cas_5_columns,
    }

    trace_coupable_yes = create_trace(
        data, column_groups, filter="yes", name="cas 4 = 18 ans et cas 5 = 17/19 ans"
    )
    trace_coupable_no = create_trace(
        data, column_groups, filter="no", name="cas 4 = 17/19 ans et cas 5 = 18 ans"
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
    fig.update_layout(**BASE_LAYOUT)
    return fig


def create_fig5(data: pd.DataFrame) -> go.Figure:
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
    fig.update_layout(**BASE_LAYOUT)
    return fig


def create_fig6(data: pd.DataFrame) -> go.Figure:
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
    fig.update_layout(**BASE_LAYOUT)
    return fig


def render(request, session) -> HttpResponse:
    from django.shortcuts import render

    data = pd.read_csv(session.csv)

    figures = []
    figures.append(create_age_fig_cases_1_to_3(data))
    figures.append(create_confidence_fig_cases_1_to_3(data))
    figures.append(create_age_fig_cases_4_and_5(data))
    figures.append(create_confidence_fig_cases_4_and_5(data))
    figures.append(create_fig5(data))
    figures.append(create_fig6(data))

    graphs = []
    for figure in figures:
        graphs.append(
            base64.b64encode(figure.to_image(format="png", width=1000)).decode("utf-8")
        )

    return render(
        request,
        template_name="experiments/session_results.html",
        context={"session": session, "graphs": graphs},
    )
