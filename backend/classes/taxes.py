from typing import ClassVar
from pydantic import BaseModel

from backend.tax.BE.dataManagerBE import *
from backend.tax.taxproperties import Canton, Taxation


class Taxes(BaseModel):
    canton: ClassVar[Canton] = Canton.BE
    place: ClassVar[str] = "Biel/Bienne"
    taxation: ClassVar[Taxation] = Taxation.single
    childrenCnt: ClassVar[int] = 0

    @classmethod
    def update_canton(cls, new_canton: Canton):
        cls.canton = new_canton
        cls.place = None
