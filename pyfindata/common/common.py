from datetime import date

import pandas as pd
from pyfindata.common.constants import ROMAN_MONTHS_MAP


def convert_roman_month_date(x: str) -> date:
    roman_month, year_ = x.split(" ")
    return date(year=int(year_), month=ROMAN_MONTHS_MAP[roman_month], day=1)


def to_index_at(data: pd.DataFrame, index_base_date: date) -> pd.DataFrame:
    if data.shape[1] != 1:
        raise ValueError("Only one-column DataFrames can be passed! ")
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("DataFrame index is not a DatetimeIndex! ")
    if pd.Timestamp(index_base_date) not in data.index:
        raise ValueError(f"Index base date: {index_base_date} not in the "
                         f"DataFrame index! ")
    col: str = data.columns[0]
    data[col] /= data.loc[index_base_date, col]
    return data
