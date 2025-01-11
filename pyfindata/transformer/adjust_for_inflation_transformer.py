from datetime import date
from typing import Final, Union

import pandas as pd

from pyfindata.common.ts_data import TSData


class AdjustForInflationTransformer:

    def __init__(
            self,
            inflation_data: TSData,
            anchor_date: Union[pd.Timestamp, date]
    ):
        if isinstance(anchor_date, date):
            anchor_date = pd.Timestamp(anchor_date)
        self._anchor_date: Final[pd.Timestamp] = anchor_date
        self._inflation_data: Final[TSData] = inflation_data

    def transform(
            self,
            data: pd.DataFrame
    ) -> pd.DataFrame:
        data = pd.merge_asof(
            left=data,
            right=self._inflation_data.data,
            direction="backward",
            left_index=True,
            right_index=True
        )

        return data


if __name__ == "__main__":

    from pyfindata.extractor.configs import CsvDataFileConfig
    from pyfindata.common.ts_config import TSConfig
    from pyfindata.common.ccy import Ccy
    from pyfindata.common.constants import DEFAULT_DATA_PATH
    from pyfindata.extractor.gus_monthly_macro_indicators_extractor import (
        GUSMonthlyMacroIndicatorsExtractor
    )
    from pyfindata.common.freq import Freq

    from pyfindata.pipeline.get_merged_stooq_data_pipeline import (
        GetMergedStooqDataPipeline
    )

    xaupln_data: pd.DataFrame = GetMergedStooqDataPipeline(
        csv_configs=[
            CsvDataFileConfig(
                ts_config=TSConfig(ticker="xaupln", ccy=Ccy.PLN),
                filepath=DEFAULT_DATA_PATH / "xaupln_pln.csv"
            )
        ],
        target_ccy=Ccy.PLN
    ).execute()

    pl_inflation = GUSMonthlyMacroIndicatorsExtractor().extract()

    adj_xaupln_data = AdjustForInflationTransformer(
        inflation_data=TSData(
            ts_config=TSConfig(
                ticker="pl_inflation", ccy=Ccy.NONE, freq=Freq.MONTHLY
            ),
            data=pl_inflation
        ),
        anchor_date=pd.Timestamp("2019-12-01")
    ).transform(data=xaupln_data)

    print(adj_xaupln_data)
