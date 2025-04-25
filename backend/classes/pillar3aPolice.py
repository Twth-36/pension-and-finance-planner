"""Class for organising pillar 3a polices"""

from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List

from backend.utils.payFrequency import PayFrequency
from .planningposition import *
from .expense import *


class Pillar3aPolice(Planningobject):
    # Object-Variables
    baseValue: Optional[float] = 0
    expPayoutValue: Optional[float] = 0
    deposit: Optional[float] = 0
    depositFreq: PayFrequency = PayFrequency.Y
    payoutDate: MonthYear

    depositExpense: Optional[Expense] = None
    payoutCF: Optional[Cashflow] = None

    # Class-variables
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} may not be negative")
        return baseValue

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Pillar3aPolice":
        obj = super().create(**data)  # Creation in Planningobjectclass

        if obj.depositExpense is None:
            param = {"name": "Einzahlung: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.depositExpense = Expense.create(**param)

        if obj.payoutCF is None:
            param = {"name": "Auszahlung: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.payoutCF = Cashflow.create(**param)

        return obj


# rebuild model to ensure other classes are loaded
Pillar3aPolice.model_rebuild()
