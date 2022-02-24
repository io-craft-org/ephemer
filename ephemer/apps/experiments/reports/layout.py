from math import ceil
from numbers import Number
from typing import Optional


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
