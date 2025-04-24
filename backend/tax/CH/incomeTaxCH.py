import math
from pathlib import Path
import pandas as pd

from backend.tax.taxproperties import Taxation


def get_dfAllein():
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "CH_alleinst_Tarife.csv"
    return pd.read_csv(file_path, delimiter=";")


def get_dfVerh():
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "CH_verh_Tarife.csv"
    return pd.read_csv(file_path, delimiter=";")


def clc_incomeTaxCH(income: float, taxation: Taxation, childrenCnt: int) -> "float":

    if taxation == Taxation.single:
        df = get_dfAllein()
    else:
        df = get_dfVerh()

    income_col, tax_col, taxper100_col = df.columns[0], df.columns[1], df.columns[2]

    if income < df[income_col][0]:
        return 0

    lower_bound = max(i for i in df[income_col] if i <= income)
    row = df[df[income_col] == lower_bound].iloc[0]

    taxes = float(row[tax_col])

    marginalRate = float(row[taxper100_col])
    income -= lower_bound
    taxes += marginalRate * math.floor(income / 100) if income >= 0 else 0

    income -= 263 * childrenCnt  # Art 36.2bis

    return taxes
