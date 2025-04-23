import os
from pathlib import Path

import pandas as pd
from backend.tax.BE import dataManagerBE
from backend.tax.taxproperties import Confession, Taxation
import csv


def clc_wealthTaxBE(wealth: float, place: str, conf: Confession):
    einfSteuer = clc_einfSteuer(wealth=wealth)
    # Kantonssteuer
    taxes = einfSteuer * dataManagerBE.taxRateBE / 100

    # Gemeindesteuer
    taxes += einfSteuer * dataManagerBE.get_taxRateCom(place=place) / 100

    # Kirchensteuer
    if conf == Confession.roem_kath:
        taxes += einfSteuer * dataManagerBE.get_taxRateRoemKath(place=place) / 100
    if conf == Confession.ev_rev:
        taxes += einfSteuer * dataManagerBE.get_taxRateEvRef(place=place) / 100
    if conf == Confession.christ_kath:
        taxes += einfSteuer * dataManagerBE.get_taxRateChristKath(place=place) / 100

    return taxes


def get_dfEinfSteuerVerm():
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "BE_verm_einfSteuer.csv"
    return pd.read_csv(file_path, delimiter=";")


def clc_einfSteuer(wealth: float) -> "float":

    df = get_dfEinfSteuerVerm()

    rate_col, wealth_col = df.columns[0], df.columns[1]

    einfSteuer = 0
    i = 0

    while (
        wealth > 1000
    ):  # according Art 42 Steuergeset BE rest-values under 100 will not be considered

        row = df.iloc[i]
        einfSteuer += min(wealth, float(row[wealth_col])) * (
            float(row[rate_col]) / 1000
        )
        wealth -= min(wealth, float(row[wealth_col]))

        i += 1

    return einfSteuer
