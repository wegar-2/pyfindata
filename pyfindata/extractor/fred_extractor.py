from datetime import date
import os
from typing import Final, Optional

import pandas as pd
import pandas_datareader.data as web

__all__ = ["FredDBExtractor"]


class FredDBExtractor:

    def __init__(
            self,
            fred_ts_id: str,
            start: date,
            end: date,
            api_key: Optional[str] = None
    ):
        if api_key is None:
            api_key = os.getenv("FRED_API_KEY")
        self._api_key: str = api_key
        self._fred_ts_id: [str] = fred_ts_id
        self._start: Final[date] = start
        self._end: Final[date] = end

    def extract(self) -> pd.DataFrame:
        data = web.DataReader(
            [self._fred_ts_id],
            'fred',
            self._start,
            self._end
        )
        return data
