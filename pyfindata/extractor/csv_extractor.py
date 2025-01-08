from pathlib import Path
from typing import Final

import pandas as pd


class CsvExtractor:

    def __init__(self, file: Path, **read_csv_kwargs):
        if not file.is_file():
            raise Exception(f"Path {file} is not a path to a file! ")
        if not file.name.endswith(".csv"):
            raise ValueError(f"Path {file} is not a path to CSV file! ")
        self._file: Final[Path] = file
        self._read_csv_kwargs: Final[dict] = read_csv_kwargs

    def extract(self) -> pd.DataFrame:
        return pd.read_csv(
            self._file,
            **self._read_csv_kwargs
        )
