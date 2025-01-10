
import pandas as pd

from pyfindata.common.ts_data import TSData


class AdjustForInflationTransformer:

    def __init__(
            self,
            inflation_data: TSData
    ):
        pass

    def transform(
            self,
            data: pd.DataFrame
    ) -> pd.DataFrame:
        pass
