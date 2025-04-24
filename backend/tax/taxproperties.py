from enum import Enum

from backend.tax.BE.dataManagerBE import get_placeNamesBE


class Canton(Enum):
    BE = "Bern"

    def get_placeNames(self):
        if self == Canton.BE:
            return get_placeNamesBE()


class Confession(Enum):
    keine_andere = "konfessionslos / andere"
    roem_kath = "römisch-katholisch"
    christ_kath = "christ-katholisch"
    ev_rev = "evangelisch-reformiert"


class Taxation(Enum):
    single = "Alleinstehenden-Satz"  # includes ledig, getrennt, geschieden, verwitwet
    together = "Verheirateten-Satz"  # includes ledig, geschieden with kids and eingetr. Partnerschaft


class TaxPositionType(Enum):
    deduction = "Steuerabzug"
    income = "Steuerliches Einkommen"
