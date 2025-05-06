from typing import ClassVar, Optional
from pydantic import BaseModel

from backend.classes.expense import Expense
from backend.tax.BE.dataManagerBE import *
from backend.tax.taxproperties import Canton, Taxation


class Taxes(BaseModel):
    canton: ClassVar[Canton] = Canton.BE
    place: ClassVar[str] = "Biel/Bienne"
    taxation: ClassVar[Taxation] = Taxation.single
    childrenCnt: ClassVar[int] = 0

    incTaxExpense: ClassVar[Optional[Expense]] = None
    wlthTaxExpense: ClassVar[Optional[Expense]] = None
    capPayoutTaxExpense: ClassVar[Optional[Expense]] = None

    @classmethod
    def update_canton(cls, new_canton: Canton):
        cls.canton = new_canton
        cls.place = None


Taxes.incTaxExpense = Expense.create(name="Einkommenssteuer", taxablePortion=0)
Taxes.wlthTaxExpense = Expense.create(name="Vermögenssteuer", taxablePortion=0)
Taxes.capPayoutTaxExpense = Expense.create(
    name="Kapitalauszahlungssteuer", taxablePortion=0
)
