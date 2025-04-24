from backend.tax.BE.wealthtaxBE import clc_wealthTaxBE
from backend.tax.taxproperties import Canton, Confession, Taxation


def clc_wealthTax(
    wealth: float,
    canton: Canton,
    place: str,
    taxation: Taxation,
    conf1: Confession,
    conf2: Confession = None,
    childrenCnt: int = 0,
):

    if taxation == Taxation.together and conf2 is None:
        raise Exception(
            "If taxation is together like a married couple, conf2 is needed as parameter"
        )
    if taxation == Taxation.single and conf2 is not None:
        raise Exception("For single taxation conf2 needs to be None")

    taxes = 0
    match canton:
        case Canton.BE:
            taxes += clc_wealthTaxBE(
                wealth=wealth,
                place=place,
                taxation=taxation,
                conf1=conf1,
                conf2=conf2,
                childrenCnt=childrenCnt,
            )

    return taxes
