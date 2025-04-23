from backend.tax.BE import incometaxBE
from backend.tax.taxproperties import Canton, Confession, Taxation


def clc_incomeTax(
    income: float, canton: Canton, place: str, taxation: Taxation, conf: Confession
):
    # TODO CH-IncomeTax
    taxes = 0
    match canton:
        case Canton.BE:
            taxes += incometaxBE.clc_incomeTaxBE(
                income=income, place=place, taxation=taxation, conf=conf
            )

    return taxes
