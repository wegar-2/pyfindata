from typing import Final

import pandas as pd


class MultiplyByTimeSeriesTransformer:

    def __init__(self, data: pd.DataFrame):
        self._data: Final[pd.DataFrame] = data
        self._multiplier_column_name: Final[str] = data.columns[0]

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        datacols: list[str] = list(data.columns)
        data = pd.merge_asof(
            left=data,
            right=self._data,
            direction="backward",
            left_index=True,
            right_index=True
        )
        datacol: str = data.columns[0]
        data[datacol] = data[datacol].ffill(axis=0).bfill(axis=0)
        for datacol in datacols:
            data[datacol] = (
                    data[datacol] * data[self._multiplier_column_name]
            )
        return data[datacols]
