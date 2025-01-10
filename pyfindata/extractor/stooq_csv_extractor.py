import logging
from typing import Union

import pandas as pd

from pyfindata.common.ts_data import TSData
from pyfindata.extractor.configs import CsvDataFileConfig
from pyfindata.extractor.constants import StooqDataModel

logger = logging.getLogger(__name__)

__all__ = ["StooqCsvExtractor"]


class StooqCsvExtractor:

    def __init__(
            self,
            csv_configs: Union[CsvDataFileConfig, list[CsvDataFileConfig]],
    ):
        if isinstance(csv_configs, CsvDataFileConfig):
            csv_configs = [CsvDataFileConfig]
        self._validate_csv_configs(csv_configs=csv_configs)
        self._csv_configs: list[CsvDataFileConfig] = csv_configs

    @staticmethod
    def _validate_csv_configs(csv_configs: list[CsvDataFileConfig]):
        if len(missing_files := [
            cfg.filepath
            for cfg in csv_configs
            if not cfg.filepath.exists() or not cfg.filepath.is_file()
        ]) > 0:
            raise Exception(
                f"Files: "
                f"{', '.join([str(file) for file in missing_files])}"
                f" either don't exist or are not files! "
            )

    def extract(self) -> list[TSData]:
        ts_datas: list[TSData] = []
        for csv_config in self._csv_configs:
            logger.info(f"Extracting & processing data "
                        f"from file {csv_config.filepath}")
            data = pd.read_csv(csv_config.filepath)
            data: pd.DataFrame = pd.DataFrame(StooqDataModel.validate(data))
            data = data.set_index("Date")
            data = data[["Close"]]
            data = data.rename(columns={"Close": "close"})
            ts_datas.append(
                TSData(data=data, ts_config=csv_config.ts_config)
            )
        return ts_datas
