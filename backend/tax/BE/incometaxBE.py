from pathlib import Path

import pandas as pd
from backend.tax.BE import dataManagerBE
from backend.tax.taxproperties import Confession, Taxation


def clc_incomeTaxBE(
    income: float,
    taxation: Taxation,
    place: str,
    conf1: Confession,
    conf2: Confession = None,
):

    if conf2:
        personcounter = 2
    else:
        personcounter = 1

    einfSteuer = clc_einfSteuer(income=income, taxation=taxation)
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


def get_dfEinfSteuerAllein():
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "BE_alleinst_einfSteuer.csv"
    return pd.read_csv(file_path, delimiter=";")


def get_dfEinfSteuerVerh():
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "BE_verh_einfSteuer.csv"
    return pd.read_csv(file_path, delimiter=";")


def clc_einfSteuer(income: float, taxation: Taxation) -> "float":
    if taxation == Taxation.single:
        df = get_dfEinfSteuerAllein()
    else:
        df = get_dfEinfSteuerVerh()

    rate_col, income_col = df.columns[0], df.columns[1]

    einfSteuer = 0
    i = 0

    while (
        income > 100
    ):  # according Art 42 Steuergeset BE rest-values under 100 will not be considered
        row = df.iloc[i]
        einfSteuer += min(income, float(row[income_col])) * (float(row[rate_col]) / 100)
        income -= min(income, float(row[income_col]))

        i += 1

    return einfSteuer
