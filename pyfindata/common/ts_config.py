from pydantic import BaseModel, ConfigDict

from pyfindata.common.ccy import Ccy
from pyfindata.common.freq import Freq


class TSConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    ticker: str
    ccy: Ccy
    freq: Freq = Freq.DAILY
