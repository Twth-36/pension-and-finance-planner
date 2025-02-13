


import os
from backend.tax.taxproperties import CivilStatus, Confession
import csv
import pandas as pd


srcledig = None
srcverheiratet = None


def clc_incomeTax(income: float, conf: Confession, civ: CivilStatus) -> "float":
    return 0

def clc_einfSteuer(income: float, conf: Confession, civ: CivilStatus) -> "float":
    if civ == CivilStatus.alleinstehend:
        
        if srcalleinstehend is None:
            file_path = os.path.join("src", "BE", "BE_alleinst_Einkommen.csv")
            srcalleinstehend = pd.read_csv(file_path)
        
    src = srcalleinstehend

    if civ == CivilStatus.verheiratet:
        
        if srcalleinstehend is None:
            file_path = os.path.join("src", "BE", "BE_verh_Einkommen.csv")
            srcalleinstehend = pd.read_csv(file_path)
        
    src = srcalleinstehend

    

