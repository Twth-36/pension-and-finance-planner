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
Income.cashflowPos = Cashflow.create(name="Übertrag Einkommen", taxablePortion=0)
