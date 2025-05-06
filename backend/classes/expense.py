"""
Class Expense for planning all possible expenses

Objects can't get created via API! see manualExpense
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from .cashflow import *
from .planningposition import *
from .incomeTaxPos import *
from .person import *


class Expense(Planningobject):
    # Object-attributes
    taxablePortion: Optional[float] = 0
    taxPosition: Optional[IncomeTaxPos] = None

    # Class-attribute
    instanceDic: ClassVar[dict] = {}
    cashflowPos: ClassVar[Cashflow]

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Expense":
        obj = super().create(**data)  # Creation in Planningobjectclass

        if obj.taxPosition is None:
            param = {"name": obj.name, "type": TaxPositionType.deduction}
            if obj.person:
                param["person"] = obj.person
            obj.taxPosition = IncomeTaxPos.create(**param)

        return obj

    @field_validator("taxPosition", mode="before")
    @classmethod
    def _load_taxPosition(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return IncomeTaxPos.get_itemByName(v["name"])
        return v


# rebuild model to ensure other classes are loaded
Expense.model_rebuild()
Expense.cashflowPos = Cashflow.create(name="Übertrag Ausgaben", taxablePortion=0)
