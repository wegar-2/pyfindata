from functools import reduce
from pathlib import Path
from typing import Final, Union

from loguru import logger
import pandas as pd

from pyfindata.common.constants import DEFAULT_DATA_PATH
from pyfindata.extractor.constants import StooqDataModel


class StooqCsvExtractor:

    def __init__(
            self,
            files: Union[str, list[str]],
            folder: Path = DEFAULT_DATA_PATH,
    ):
        if not folder.is_dir():
            raise Exception(f"Path {folder} does not point at a directory")
        self._folder: Final[Path] = folder

        if isinstance(files, str):
            files = [files]
        self._validate_files(files=files)
        self._files: list[str] = files

    def _validate_files(self, files: list[str]):
        folder_files: list[str] = [
            x.name[:-4] for x in self._folder.glob("*.csv")
        ]
        if len(missing_files := [
            x for x in files if x not in folder_files
        ]) > 0:
            raise Exception(f"Files: {', '.join(missing_files)} are not "
                            f"available in the data folder! ")

    def extract(self) -> pd.DataFrame:
        datas: list[pd.DataFrame] = []
        for file in self._files:
            with self._folder / f"{file}.csv" as fpath:
                logger.info(f"Extracting data ")
                data = pd.read_csv(fpath)
                data: pd.DataFrame = pd.DataFrame(StooqDataModel.validate(data))
                data = data.set_index("Date")
                data = data[["Close"]]
                data = data.rename(columns={"Close": file})
                datas.append(data)

        data = reduce(
            lambda left, right: pd.merge(
                left=left, right=right, left_index=True, right_index=True,
                how="outer"
            ),
            datas
        )
        return data.ffill(axis=0).bfill(axis=0)
