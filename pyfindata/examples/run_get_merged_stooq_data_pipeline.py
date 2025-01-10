from pyfindata.common.ccy import Ccy
from pyfindata.common.ts_config import TSConfig
from pyfindata.extractor.configs import CsvDataFileConfig
from pyfindata.common.freq import Freq
from pyfindata.common.constants import DEFAULT_DATA_PATH
from pyfindata.pipeline.get_merged_stooq_data_pipeline import (
    GetMergedStooqDataPipeline
)


if __name__ == "__main__":

    ts_configs: list[TSConfig] = [
        TSConfig(ticker="apple", ccy=Ccy.USD, freq=Freq.DAILY),
        TSConfig(ticker="btc", ccy=Ccy.PLN, freq=Freq.DAILY),
        TSConfig(ticker="dax", ccy=Ccy.EUR, freq=Freq.DAILY),
        TSConfig(ticker="eth", ccy=Ccy.USD, freq=Freq.DAILY),
        TSConfig(ticker="eurpln", ccy=Ccy.PLN, freq=Freq.DAILY),
        TSConfig(ticker="nasdaq", ccy=Ccy.USD, freq=Freq.DAILY),
        TSConfig(ticker="nvidia", ccy=Ccy.USD, freq=Freq.DAILY),
        TSConfig(ticker="sp500", ccy=Ccy.USD, freq=Freq.DAILY),
        TSConfig(ticker="tesla", ccy=Ccy.USD, freq=Freq.DAILY),
        TSConfig(ticker="tsmc", ccy=Ccy.USD, freq=Freq.DAILY),
        TSConfig(ticker="usdpln", ccy=Ccy.PLN, freq=Freq.DAILY),
        TSConfig(ticker="xaupln", ccy=Ccy.PLN, freq=Freq.DAILY),
    ]

    csv_configs: list[CsvDataFileConfig] = [
        CsvDataFileConfig(
            ts_config=ts_config,
            filepath=(
                    DEFAULT_DATA_PATH /
                    f"{ts_config.ticker}_{ts_config.ccy.value}.csv"
            )
        )
        for ts_config in ts_configs
    ]

    pipeline = GetMergedStooqDataPipeline(
        csv_configs=csv_configs
    )

    data = pipeline.execute()
    print(data)
