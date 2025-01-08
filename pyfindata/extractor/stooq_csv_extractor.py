from pathlib import Path

import pandas as pd

from pyfindata.extractor.csv_extractor import CsvExtractor
from pathlib import Path
from typing import Final, Union

from loguru import logger
import pandas as pd


class StooqCsvExtractor:

    def __init__(
            self,
            folder: Path,
            files: Union[str, list[str]]
    ):
        if not folder.is_dir():
            raise Exception(f"Path {folder} does not point at a directory")
        self._folder: Final[Path] = folder

        if isinstance(files, str):
            files = [files]
        self._validate_files(files=files)
        self._files: list[str] = files

    def _validate_files(self, files: list[str]):
        with [
            x.name[:-4] for x in self._folder.glob(".csv")
        ] as folder_files:
            if len(missing_files := [
                x for x in files if x not in folder_files
            ]) > 0:
                raise Exception(f"Files: {', '.join(missing_files)} are not "
                                f"available in the data folder! ")

    def extract(self) -> dict[str, pd.DataFrame]:
        datas: dict[str, pd.DataFrame] = {}
        for file in self._files:
            with self._folder / f"{file}.csv" as fpath:
                logger.info(f"Extracting data ")
                data = pd.read_csv(fpath)

                datas[file] = data
        return datas
