from typing import Final
from pathlib import Path


DEFAULT_DATA_PATH: Final[Path] = Path(__file__).parent.parent.parent / "data"

ROMAN_MONTHS_MAP: Final[dict[str, int]] = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
    "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12
}
