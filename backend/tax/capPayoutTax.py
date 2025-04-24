from backend.tax.BE.capPayoutTaxBE import clc_capPayoutTaxBE
from backend.tax.CH.capPayoutTaxCH import clc_capPayoutTaxCH
from backend.tax.taxproperties import Canton, Confession, Taxation


def clc_capPayoutTax(
    payoutValue: float,
    canton: Canton,
    place: str,
    taxation: Taxation,
    conf1: Confession,
    conf2: Confession = None,
    childrenCnt: int = 0,
):

    if taxation == Taxation.single and conf2 is not None:
        raise Exception("For single taxation conf2 needs to be None")

    taxes = clc_capPayoutTaxCH(
        payoutValue=payoutValue, taxation=taxation, childrenCnt=childrenCnt
    )
    match canton:
        case Canton.BE:
            taxes += clc_capPayoutTaxBE(
                payoutValue=payoutValue,
                place=place,
                taxation=taxation,
                conf1=conf1,
                conf2=conf2,
            )

    return taxes
