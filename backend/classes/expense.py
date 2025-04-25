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


# rebuild model to ensure other classes are loaded
Expense.model_rebuild()
