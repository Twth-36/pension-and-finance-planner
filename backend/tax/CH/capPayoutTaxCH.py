import math
from pathlib import Path
import pandas as pd

from backend.tax.CH.incomeTaxCH import clc_incomeTaxCH
from backend.tax.taxproperties import Taxation


def clc_capPayoutTaxCH(
    payoutValue: float, taxation: Taxation, childrenCnt: int = 0
) -> "float":

    # According Art. 38 Bundesgesetz über die direkte Budnesteuer one fifth of the incomeTax
    return (
        clc_incomeTaxCH(
            income=payoutValue, taxation=Taxation.single, childrenCnt=childrenCnt
        )
        / 5
    )
