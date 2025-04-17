from pathlib import Path
import pandas as pd


def get_placeNamesBE():

    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "SteueranlagenGDE.csv"
    df = pd.read_csv(file_path, delimiter=";")
    return df["Gde Name"].dropna().unique().tolist()
