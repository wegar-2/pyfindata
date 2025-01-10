from typing import Final, Optional, Literal

from pathlib import Path

import pandas as pd


class NBPRealEstatePricesExtractor:

    _XLSX_URL: Final[str] = (
        "https://static.nbp.pl/dane/rynek-nieruchomosci/ceny_mieszkan.xlsx"
    )

    _RELEVANT_COLUMNS: Final[list[str]] = [
        'Kwartał', 'Białystok', 'Bydgoszcz', 'Gdańsk', 'Gdynia', 'Katowice',
        'Kielce', 'Kraków', 'Lublin', 'Łódź', 'Olsztyn', 'Opole', 'Poznań',
        'Rzeszów', 'Szczecin', 'Warszawa', 'Wrocław', 'Zielona Góra',
        '7 miast', '10 miast', '6 miast bez Warszawy'
    ]

    _SHEET_NAMES_MAP: Final[dict[str]] = {
        "primary": "Rynek pierwotny", "secondary": "Rynek wtórny"
    }

    def _extract_sheet(
            self,
            sheet_name: Literal["primary", "secondary"]
    ) -> pd.DataFrame:
        data = pd.read_excel(
            self._XLSX_URL, sheet_name=self._SHEET_NAMES_MAP[sheet_name]
        )
        offer_prices = (
            data.iloc[:, :].loc[:, self._RELEVANT_COLUMNS]
        )
        transactional_prices = (
            data.iloc[:, :].loc[:, self._RELEVANT_COLUMNS]
        )

        data = pd.concat()
        return data

    def extract(self) -> pd.DataFrame:
        primary = self._extract_sheet(sheet_name="primary")
        secondary = self._extract_sheet(sheet_name="secondary")
        # data.columns = pd.MultiIndex.from_product(
        #     [
        #
        #     ]
        # )

        return pd.DataFrame()


if __name__ == "__main__":

    NBPRealEstatePricesExtractor().extract()
