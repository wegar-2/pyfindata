from datetime import date
from typing import Final

import pandas as pd


class FilterDatesRangeTransformer:

    def __init__(self, start: date, end: date):
        self._start: Final[date] = start
        self._end: Final[date] = end

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        return data[self._start:self._end]
