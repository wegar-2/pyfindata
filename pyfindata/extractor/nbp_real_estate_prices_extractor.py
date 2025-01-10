from typing import Final, Literal, TypeAlias

from unidecode import unidecode
from pyfindata.common.common import convert_roman_month_date

import pandas as pd

Market: TypeAlias = Literal["primary", "secondary"]
PriceType: TypeAlias = Literal["transactional", "offer"]


class NBPRealEstatePricesExtractor:

    _XLSX_URL: Final[str] = (
        "https://static.nbp.pl/dane/rynek-nieruchomosci/ceny_mieszkan.xlsx"
    )

    _RELEVANT_COLUMNS: Final[list[str]] = [
        'Kwartał',
        'Białystok', 'Bydgoszcz', 'Gdańsk', 'Gdynia', 'Katowice',
        'Kielce', 'Kraków', 'Lublin', 'Łódź', 'Olsztyn', 'Opole', 'Poznań',
        'Rzeszów', 'Szczecin', 'Warszawa', 'Wrocław', 'Zielona Góra',
        '7 miast', '10 miast', '6 miast bez Warszawy'
    ]

    _SHEET_NAMES_MAP: Final[dict[str]] = {
        "primary": "Rynek pierwotny", "secondary": "Rynek wtórny"
    }

    def _get_english_colnames(self) -> list[str]:
        return ["quarter"] + [
            unidecode(x.lower()) for x in self._RELEVANT_COLUMNS[1:18]
        ] + [
            "7cities", "10cities", "6cities_without_warsaw"
        ]

    def _format_data(
            self,
            data: pd.DataFrame,
            price_type: PriceType
    ) -> pd.DataFrame:
        data = data.rename(columns=dict(zip(
            self._RELEVANT_COLUMNS, self._get_english_colnames()
        )))
        data = data.loc[~data["quarter"].isna(), :]
        data["quarter"] = [
            convert_roman_month_date(x=x) for x in data["quarter"]
        ]
        data = data.set_index("quarter")
        data.columns = pd.MultiIndex.from_product([
            [price_type], list(data.columns)
        ])
        return data

    def _extract_sheet(
            self,
            sheet_name: Market
    ) -> pd.DataFrame:
        data = pd.read_excel(
            self._XLSX_URL,
            sheet_name=self._SHEET_NAMES_MAP[sheet_name],
            skiprows=6
        )

        offer_prices = data.iloc[:, :22].loc[:, self._RELEVANT_COLUMNS]
        transactional_prices = data.iloc[:, 23:44]
        transactional_prices.columns = [
            x.split(".")[0] for x in transactional_prices.columns
        ]
        transactional_prices = transactional_prices.rename(columns={
            "Gdynia*": "Gdynia"
        })
        transactional_prices = (
            transactional_prices.loc[:, self._RELEVANT_COLUMNS]
        )
        data = pd.merge(
            left=self._format_data(
                data=offer_prices,
                price_type="offer"
            ),
            right=self._format_data(
                data=transactional_prices,
                price_type="transactional"
            ),
            left_index=True,
            right_index=True,
            how="inner"
        )
        data = data.ffill(axis=0).bfill(axis=1)
        return data

    def extract(self) -> pd.DataFrame:
        primary = self._extract_sheet(sheet_name="primary")
        secondary = self._extract_sheet(sheet_name="secondary")
        primary.columns = pd.MultiIndex.from_tuples(
            [("primary", x[0], x[1]) for x in primary.columns],
            names=["market", "price_type", "location"]
        )
        secondary.columns = pd.MultiIndex.from_tuples(
            [("secondary", x[0], x[1]) for x in secondary.columns],
            names=["market", "price_type", "location"]
        )
        data = pd.merge(
            left=primary,
            right=secondary,
            left_index=True,
            right_index=True,
            how="inner"
        )
        return data


