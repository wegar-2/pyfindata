from pyfindata.extractor.gus_monthly_macro_indicators_extractor import (
    GUSMonthlyMacroIndicatorsExtractor
)

if __name__ == "__main__":
    res = GUSMonthlyMacroIndicatorsExtractor().extract()
    print(res)
