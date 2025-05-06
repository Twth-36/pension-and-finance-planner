"""Class for organising pillar 3b polices"""

from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List

from backend.utils.payFrequency import PayFrequency
from .planningposition import *
from .expense import *
from .income import *


class Pillar3bPolice(Planningobject):
    # Object-Variables

    baseValue: Optional[float] = 0
    expPayoutValue: Optional[float] = 0
    expPensionValue: Optional[float] = 0  # monthly
    deposit: Optional[float] = 0
    depositFreq: PayFrequency = PayFrequency.Y
    payoutDate: MonthYear

    depositExpense: Optional[Expense] = None
    payoutCF: Optional[Cashflow] = None
    pensionIncome: Optional[Income] = None

    # Class-variables
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} may not be negative")
        return baseValue

    @field_validator("depositExpense", mode="before")
    @classmethod
    def _load_depositExpense(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Expense.get_itemByName(v["name"])
        return v

    @field_validator("payoutCF", mode="before")
    @classmethod
    def _load_payoutCF(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Cashflow.get_itemByName(v["name"])
        return v

    @field_validator("pensionIncome", mode="before")
    @classmethod
    def _load_pensionIncome(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Income.get_itemByName(v["name"])
        return v

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Pillar3bPolice":
        obj = super().create(**data)  # Creation in Planningobjectclass

        if obj.depositExpense is None:
            param = {"name": "Einzahlung: " + obj.name, "taxablePortion": 0}
            if obj.person:
                param["person"] = obj.person
            obj.depositExpense = Expense.create(**param)

        if obj.payoutCF is None:
            param = {"name": "Auszahlung: " + obj.name, "taxablePortion": 0}
            if obj.person:
                param["person"] = obj.person
            obj.payoutCF = Cashflow.create(**param)

        if obj.pensionIncome is None:
            param = {"name": "Rente: " + obj.name, "taxablePortion": 0}
            if obj.person:
                param["person"] = obj.person
            obj.pensionIncome = Income.create(**param)

        return obj


# rebuild model to ensure other classes are loaded
Pillar3bPolice.model_rebuild()
