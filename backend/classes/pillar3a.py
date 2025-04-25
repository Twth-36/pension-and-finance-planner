"""Class for organising pillar 3a"""

from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List
from .planningposition import *
from .expense import *


class Pillar3a(Planningobject):
    # Object-Variables
    baseValue: Optional[float] = 0
    returnRate: Optional[float] = 0
    deposit: Optional[List[Planningposition]] = []
    payoutDate: Optional[List[Planningposition]] = (
        []
    )  # Value not used (only scenario and month)

    depositExpense: Optional[Expense] = (
        None  # expense Position where deposits are accounted
    )
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
    def create(cls, **data) -> "Pillar3a":
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
Pillar3a.model_rebuild()
