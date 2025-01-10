from functools import reduce
import logging
from typing import Final

import pandas as pd

from pyfindata.common.ccy import Ccy
from pyfindata.common.ts_data import TSData
from pyfindata.common.ts_config import TSConfig
from pyfindata.extractor.stooq_csv_extractor import StooqCsvExtractor
from pyfindata.extractor.configs import CsvDataFileConfig
from pyfindata.transformer.convert_to_currency_transformer import (
    ConvertToCurrencyTransformer
)

logger = logging.getLogger(__name__)

__all__ = ["GetMergedStooqDataPipeline"]


class GetMergedStooqDataPipeline:

    def __init__(
            self,
            csv_configs: list[CsvDataFileConfig],
            target_ccy: Ccy = Ccy.PLN
    ):
        self._csv_configs: Final[list[CsvDataFileConfig]] = csv_configs
        self._extractor: Final[StooqCsvExtractor] = (
            StooqCsvExtractor(csv_configs=self._csv_configs)
        )
        self._target_ccy: Final[Ccy] = target_ccy
        self._unique_data_ccys: list[Ccy] = self._extract_unique_data_ccys(
            csv_configs=self._csv_configs
        )

    def _extract_unique_data_ccys(
            self,
            csv_configs: list[CsvDataFileConfig]
    ) -> list[Ccy]:
        return list(set([
            csv_config.ts_config.ccy
            for csv_config in csv_configs
            if csv_config.ts_config.ccy not in [self._target_ccy, Ccy.NONE]
        ]))

    def execute(self) -> pd.DataFrame:
        logger.info("Extracting Stooq data from CSV files")
        ts_datas: list[TSData] = self._extractor.extract()

        logger.info(f"Converting data to currency: {self._target_ccy}")
        converted_ts_datas: list[TSData] = [
            ts_data
            for ts_data in ts_datas
            if (ts_data.ts_config.ccy == Ccy.NONE or
                ts_data.ts_config.ccy == self._target_ccy)
        ]
        for ccy in self._unique_data_ccys:
            currency_pair: str = f"{ccy.value}{self._target_ccy.value}"
            logger.info(f"Performing conversions from: {ccy}")
            ccy_ts_data = [
                ts_data
                for ts_data in ts_datas
                if ts_data.ts_config.ticker == currency_pair
            ]
            if len(ccy_ts_data) == 0:
                raise Exception(
                    f"No data available to perform currency conversion "
                    f"invloving pair {currency_pair}"
                )

            converter = ConvertToCurrencyTransformer(
                from_ccy=ccy,
                to_ccy=self._target_ccy,
                ts_data=ccy_ts_data[0]
            )

            for ts_data in ts_datas:
                if ts_data.ts_config.ccy == ccy:
                    logger.info(f"Converting currency for time series: "
                                f"{ts_data.ts_config}")
                    converted_ts_datas.append(
                        converter.transform(ts_data=ts_data)
                    )

        logger.info("Joining the converted data")
        datas_to_merge = []
        for ts_data in converted_ts_datas:
            data_piece = ts_data.data.copy(deep=True)
            data_piece.columns = pd.MultiIndex.from_arrays([
                [f"{ts_data.ts_config.ticker}"],
                [f"{ts_data.ts_config.ccy.value}"]
            ])
            datas_to_merge.append(data_piece)
        data = reduce(
            lambda left, right: pd.merge(
                left=left,
                right=right,
                left_index=True,
                right_index=True,
                how="outer"
            ),
            datas_to_merge
        )
        return data.ffill(axis=0).bfill(axis=0)
