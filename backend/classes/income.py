"""
Class Income for planning all possible incomes

Objects can't get created via API! see manualIncome
"""

from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List

from backend.classes.planningobject import Planningobject
from .cashflow import Cashflow
from .planningposition import *
from .person import *
from .incomeTaxPos import *
from .scenario import *


class Income(Planningobject):
    # Object-attributes
    taxablePortion: Optional[float] = 100
    taxPosition: Optional[IncomeTaxPos] = None

    # Class-attribute
    instanceDic: ClassVar[dict] = {}
    cashflowPos: ClassVar[Cashflow] = None  # cashlowposition on which the total flows

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Income":
        obj = super().create(**data)  # Creation in Planningobjectclass

        if obj.taxPosition is None:
            param = {"name": obj.name, "type": TaxPositionType.income}
            if obj.person:
                param["person"] = obj.person
            obj.taxPosition = IncomeTaxPos.create(**param)

        return obj


# rebuild model to ensure other classes are loaded
Income.model_rebuild()
