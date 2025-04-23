from typing import ClassVar
from pydantic import BaseModel

from backend.tax.BE.dataManagerBE import *
from backend.tax.taxproperties import Canton, Taxation


class Taxes(BaseModel):
    canton: ClassVar[Canton] = Canton.BE
    place: ClassVar[str] = "Bern"
    taxation: ClassVar[Taxation] = Taxation.single
    baseYearTaxCalc: ClassVar[int] = 2025

    @classmethod
    def update_canton(cls, new_canton: Canton):
        cls.canton = new_canton
        cls.place = None
