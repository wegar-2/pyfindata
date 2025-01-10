from pathlib import Path

from pydantic import BaseModel, ConfigDict, field_validator

from pyfindata.common.ts_config import TSConfig


class CsvDataFileConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    ts_config: TSConfig
    filepath: Path

    @field_validator("filepath", mode="before") # noqa
    @classmethod
    def _validate_filepath(cls, value):
        if not value.name.endswith(".csv"):
            raise ValueError(
                f"Invalid filepath {value} encountered when creating "
                f"{cls.__name__} instance: not a CSV file path"
            )
        return value
