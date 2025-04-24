from pathlib import Path

import pandas as pd
from backend.tax.BE import dataManagerBE
from backend.tax.taxproperties import Confession, Taxation


def clc_wealthTaxBE(
    wealth: float,
    taxation: Taxation,
    place: str,
    conf1: Confession,
    conf2: Confession = None,
    childrenCnt: int = 0,
):

    if conf2:
        personcounter = 2
    else:
        personcounter = 1

    # Reduction according to Art 64 Steuergesetz Kt Bern
    if taxation == Taxation.together:
        wealth -= 18000  # Art 64 b
    wealth -= childrenCnt * 18000  # Art 64a

    einfSteuer = clc_einfSteuer(wealth=wealth)
    # Kantonssteuer
    taxes = einfSteuer * dataManagerBE.taxRateBE

    # Gemeindesteuer
    taxes += einfSteuer * dataManagerBE.get_taxRateCom(place=place)

    # Kirchensteuer Person1
    match conf1:
        case Confession.roem_kath:
            taxes += (
                einfSteuer
                * dataManagerBE.get_taxRateRoemKath(place=place)
                / personcounter
            )  # in case only one of two person belongs a specific confession, the churchtax gets halfed

        case Confession.ev_rev:
            taxes += (
                einfSteuer * dataManagerBE.get_taxRateEvRef(place=place) / personcounter
            )

        case Confession.christ_kath:
            taxes += (
                einfSteuer
                * dataManagerBE.get_taxRateChristKath(place=place)
                / personcounter
            )

    # Kirchensteuer Person2
    match conf2:
        case Confession.roem_kath:
            taxes += (
                einfSteuer
                * dataManagerBE.get_taxRateRoemKath(place=place)
                / personcounter
            )  # in case only one of two person belongs a specific confession, the churchtax gets halfed

        case Confession.ev_rev:
            taxes += (
                einfSteuer * dataManagerBE.get_taxRateEvRef(place=place) / personcounter
            )

        case Confession.christ_kath:
            taxes += (
                einfSteuer
                * dataManagerBE.get_taxRateChristKath(place=place)
                / personcounter
            )

    return taxes


def get_dfEinfSteuerVerm():
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "BE_verm_einfSteuer.csv"
    return pd.read_csv(file_path, delimiter=";")


def clc_einfSteuer(wealth: float) -> "float":

    if wealth < 100000:  # Art 65 3
        return 0

    df = get_dfEinfSteuerVerm()

    rate_col, wealth_col = df.columns[0], df.columns[1]

    einfSteuer = 0
    i = 0

    while (
        wealth > 1000
    ):  # according Art 65 Steuergeset BE rest-values under 1000 will not be considered

        row = df.iloc[i]
        einfSteuer += min(wealth, float(row[wealth_col])) * (
            float(row[rate_col]) / 1000
        )
        wealth -= min(wealth, float(row[wealth_col]))

        i += 1

    return einfSteuer
