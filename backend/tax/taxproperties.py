from enum import Enum


class Canton(Enum):
    BE = "Bern"
    BS = "Basel Stadt"


class Confession(Enum):
    keine_andere = "konfessionslos / andere"
    roem_kath = "römisch-katholisch"
    christ_kath = "christ-katholisch"
    ev_rev = "evangelisch-reformiert"


class Taxation(Enum):
    single = "Einzelne Besteuerung"  # includes ledig, getrennt, geschieden, verwitwet
    together = "Gemeinsame Besteuerung"


class TaxPositionType(Enum):
    deduction = "Steuerabzug"
    income = "Steuerliches Einkommen"
