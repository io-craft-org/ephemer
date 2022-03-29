import base64
from dataclasses import dataclass
from math import ceil
from numbers import Number
from typing import Optional

import pandas as pd
from plotly import graph_objs as go

BASE_LAYOUT = {
    "font_size": 20,
    "barmode": "group",
    "bargap": 0.6,
    "margin": dict(t=50, b=50),
}


@dataclass
class Graphique:
    figure: go.Figure
    title: str
    legend: Optional[str] = None


def compute_bounds(
    values,
    zero_lower_bound: Optional[bool] = None,
    minimal_range: Number = 1,
    precision: Number = 0.1,
):
    if zero_lower_bound:
        lower_bound = 0
        max_value = max(values)
        upper_bound = max_value * 1.2
    else:
        min_value = min(values)
        max_value = max(values)
        diff = max(max_value - min_value, minimal_range)
        upper_bound = min_value + diff * (1 + 15 / 55)
        lower_bound = min_value - diff * 30 / 55
    if minimal_range:
        upper_bound = max(upper_bound, lower_bound + minimal_range)

    def round_at_precision(n):
        return ceil(n / precision) * precision

    return round_at_precision(lower_bound), round_at_precision(upper_bound)


def filter_valid_participants(data: pd.DataFrame) -> pd.DataFrame:
    return data[
        data["participant._index_in_pages"] >= data["participant._max_page_index"]
    ]


def render_graphs(csv_file, graph_funcs):
    data = filter_valid_participants(pd.read_csv(filepath_or_buffer=csv_file))
    graphs = []
    for func in graph_funcs:
        result = func(data)
        if not isinstance(result, list):
            result = [result]
        for graph in result:
            graph.figure.update_layout(**BASE_LAYOUT)
            graphs.append(
                {
                    "image": base64.b64encode(
                        graph.figure.to_image(format="png", width=1200)
                    ).decode("utf-8"),
                    "legend": graph.legend,
                    "title": graph.title,
                }
            )
    return graphs
