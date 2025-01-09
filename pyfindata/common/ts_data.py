import pandas as pd
from pydantic import BaseModel, ConfigDict

from pyfindata.common.ts_config import TSConfig


class TSData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    ts_config: TSConfig
    data: pd.DataFrame
