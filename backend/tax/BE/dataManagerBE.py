from pathlib import Path
import pandas as pd

taxRateBE = 2.975


def get_dfSteueranlagenGDE():
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "SteueranlagenGDE.csv"
    return pd.read_csv(file_path, delimiter=";")


def get_placeNamesBE():
    df = get_dfSteueranlagenGDE()
    return sorted(df["Gde Name"].dropna().unique().tolist())


def get_taxRateCom(place: str):
    df = get_dfSteueranlagenGDE()
    row = df[df["Gde Name"] == place]

    if row.empty:
        raise ValueError(f"Community '{place}' not found in the data.")

    return float(row.iloc[0]["Anlage Gde NP"])


def get_taxRateRoemKath(place: str):
    df = get_dfSteueranlagenGDE()
    row = df[df["Gde Name"] == place]

    if row.empty:
        raise ValueError(f"Community '{place}' not found in the data.")

    return float(row.iloc[0]["römisch-katholisch"])


def get_taxRateChristKath(place: str):
    df = get_dfSteueranlagenGDE()
    row = df[df["Gde Name"] == place]

    if row.empty:
        raise ValueError(f"Community '{place}' not found in the data.")

    return float(row.iloc[0]["christ-katholisch"])


def get_taxRateEvRef(place: str):
    df = get_dfSteueranlagenGDE()
    row = df[df["Gde Name"] == place]

    if row.empty:
        raise ValueError(f"Community '{place}' not found in the data.")

    return float(row.iloc[0]["reformiert"])
