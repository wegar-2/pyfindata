from typing import Final

import numpy as np
import pandas as pd


class GUSMonthlyMacroIndicatorsExtractor:

    _URL: Final[str] = (
        "https://stat.gov.pl/download/gfx/portalinformacyjny/pl/"
        "defaultstronaopisowa/1772/2/1/"
        "wybrane_miesieczne_wskazniki_makroekonomiczne_cz_i.xlsx"
    )

    def extract(self) -> pd.DataFrame:
        data = pd.read_excel(
            self._URL,
            sheet_name="WSKAŹNIKI CEN"
        )
        data_index = data.iloc[2:4, 3:].T.reset_index(drop=True).rename(
            columns={2: "year", 3: "month"}
        )
        data_index["year"] = data_index["year"].ffill(axis=0).astype(np.int64)
        data_index = data_index.loc[~data_index["month"].isna(), :]
        data_index.loc[:, "month"] = data_index["month"].astype(np.int64)
        data_index.loc[:, "yearmon"] = data_index.apply(
            lambda x: pd.Timestamp(year=x["year"], month=x["month"], day=1),
            axis=1
        )
        data_index = data_index.loc[:, ["yearmon"]]
        cpi_data = data.iloc[39:41, 1:].T.reset_index(drop=True)
        cpi_data.columns = ["CPI_YoY", "CPI_MoM"]
        cpi_data = cpi_data.loc[2:, :].reset_index(drop=True)
        cpi_data = cpi_data.loc[:data_index.index[-1], :]
        return pd.concat([data_index, cpi_data], axis=1)
