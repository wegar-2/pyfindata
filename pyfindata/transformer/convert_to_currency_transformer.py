from typing import Final

import pandas as pd

from pyfindata.common.ccy import Ccy
from pyfindata.common.ts_data import TSData
from pyfindata.common.ts_config import TSConfig


class ConvertToCurrencyTransformer:

    def __init__(
            self,
            from_ccy: Ccy,
            to_ccy: Ccy,
            ts_data: TSData
    ):
        self._from_ccy: Final[Ccy] = from_ccy
        self._to_ccy: Final[Ccy] = to_ccy
        self._ts_data: Final[TSData] = ts_data

    def transform(self, ts_data: TSData) -> TSData:
        data: pd.DataFrame

        return TSData(
            ts_config=TSConfig(
                ticker=ts_data.ts_config.ticker,
                ccy=self._to_ccy,
                freq=ts_data.ts_config.freq
            ),
            data=data
        )
    