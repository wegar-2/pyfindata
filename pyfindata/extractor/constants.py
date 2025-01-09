import pandas as pd
import pandera as pa
from pandera.typing import Series


class StooqDataModel(pa.DataFrameModel):
    Date: Series[pd.Timestamp] = pa.Field(coerce=True)
    Open: Series[float] = pa.Field(ge=0, coerce=True)
    High: Series[float] = pa.Field(ge=0, coerce=True)
    Low: Series[float] = pa.Field(ge=0, coerce=True)
    Close: Series[float] = pa.Field(ge=0, coerce=True)
    # Volume: Series[float] = pa.Field(ge=0, coerce=True)
