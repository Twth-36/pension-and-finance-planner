from backend.tax.BE import incomeTaxBE
from backend.tax.CH.incomeTaxCH import clc_incomeTaxCH
from backend.tax.taxproperties import Canton, Confession, Taxation


def clc_incomeTax(
    income: float,
    canton: Canton,
    place: str,
    taxation: Taxation,
    conf1: Confession,
    conf2: Confession = None,
    childrenCnt: int = 0,
):

    if taxation == Taxation.single and conf2 is not None:
        raise Exception("For single taxation conf2 needs to be None")

    taxes = clc_incomeTaxCH(income=income, taxation=taxation, childrenCnt=childrenCnt)
    match canton:
        case Canton.BE:
            taxes += incomeTaxBE.clc_incomeTaxBE(
                income=income, place=place, taxation=taxation, conf1=conf1, conf2=conf2
            )

    return taxes
