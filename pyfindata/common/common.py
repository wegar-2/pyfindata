from datetime import date

from pyfindata.common.constants import ROMAN_MONTHS_MAP


def convert_roman_month_date(x: str) -> date:
    roman_month, year_ = x.split(" ")
    return date(year=int(year_), month=ROMAN_MONTHS_MAP[roman_month], day=1)
