from typing import ClassVar
from pydantic import BaseModel

from backend.tax.taxproperties import Canton, Taxation


class Taxes(BaseModel):
    canton: ClassVar[Canton] = None
    place: ClassVar[str] = None
    place: ClassVar[str] = None
    taxation: ClassVar[Taxation] = Taxation.single

    taxRateCanton: ClassVar[float] = 0
    taxRateCom: ClassVar[float] = 0
    taxRateRoem_kath: ClassVar[float] = 0
    taxRateEv_ref: ClassVar[float] = 0
    baseYearTaxCalc: int = 2025
