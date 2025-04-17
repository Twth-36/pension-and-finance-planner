from typing import ClassVar
from pydantic import BaseModel

from backend.tax.taxproperties import Canton, Taxation


class Taxes(BaseModel):
    canton: ClassVar[Canton] = Canton.BE
    place: ClassVar[str] = None
    taxation: ClassVar[Taxation] = Taxation.single

    taxRateCanton: ClassVar[float] = None
    taxRateCom: ClassVar[float] = None
    taxRateRoem_kath: ClassVar[float] = None
    taxRateEv_ref: ClassVar[float] = None
    taxRateChrist_kath: ClassVar[float] = None
    baseYearTaxCalc: ClassVar[int] = 2025

    @classmethod
    def update_canton(cls, new_canton: Canton):
        cls.canton = new_canton
        cls.taxRateCanton = None

        cls.place = None
        cls.taxRateRoem_kath = None
        cls.taxRateEv_ref = None
        cls.taxRateChrist_kath = None

    @classmethod
    def update_place(cls, new_place: str):
        cls.place = new_place
