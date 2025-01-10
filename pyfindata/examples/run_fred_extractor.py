from datetime import date

from pyfindata.extractor.fred_extractor import FredDBExtractor


if __name__ == "__main__":
    res = FredDBExtractor(
        fred_ts_id="CPIAUCSL",
        start=date(2000, 1, 1),
        end=date(2024, 12, 1)
    ).extract()

    print(res)
