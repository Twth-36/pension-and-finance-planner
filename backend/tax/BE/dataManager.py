import pandas as pd


def get_communes(file_path):
    df = pd.read_csv(file_path, delimiter=";")
    return df["Gde Name"].dropna().unique().tolist()
