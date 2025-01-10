from pyfindata.extractor.nbp_real_estate_prices_extractor import (
    NBPRealEstatePricesExtractor
)


if __name__ == "__main__":

    res = NBPRealEstatePricesExtractor().extract()

    print(res)
