"""realEstates inlcusive renovations etc."""

from typing import Optional, List
from .planningposition import *  # issue why necessary?
from pydantic import BaseModel, field_validator
from ..utils.monthYear import *
from .expense import *
from .person import *
from .scenario import *


class RealEstate(Planningobject):
    # Object-variable

    baseValue: Optional[float] = 0

    baseTaxValue: Optional[float] = None
    taxValue: Optional[List[Planningposition]] = []
    taxRate: Optional[float] = None
    taxExpense: Optional[Expense] = None

    maintCostRate: float = None
    maintenanceExpense: Optional[Expense] = None

    renovations: Optional[List[Planningposition]] = []
    renovationExpense: Optional[Expense] = None

    purchase: Optional[List[Planningposition]] = []
    purchaseCF: Optional[Cashflow] = None

    sale: Optional[List[Planningposition]] = []
    saleCF: Optional[Cashflow] = None

    # Class-variable
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} is strict smaller than 0")
        return baseValue

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "RealEstate":
        obj = super().create(**data)  # Creation in Planningobjectclass

        if obj.taxExpense is None:
            param = {"name": "Liegenschaftssteuer: " + obj.name, "taxablePortion": 0}
            if obj.person:
                param["person"] = obj.person
            obj.taxExpense = Expense.create(**param)

        if obj.maintenanceExpense is None:
            param = {"name": "Unterhaltskosten: " + obj.name, "taxablePortion": 0}
            if obj.person:
                param["person"] = obj.person
            obj.maintenanceExpense = Expense.create(**param)

        if obj.renovationExpense is None:
            param = {"name": "Renovationen: " + obj.name, "taxablePortion": 0}
            if obj.person:
                param["person"] = obj.person
            obj.renovationExpense = Expense.create(**param)

        if obj.purchaseCF is None:
            param = {"name": "Kauf / Investition: " + obj.name}
            if obj.person:
                param["person"] = obj.person
            obj.purchaseCF = Cashflow.create(**param)

        if obj.saleCF is None:
            param = {"name": "Verkauf: " + obj.name}
            if obj.person:
                param["person"] = obj.person
            obj.saleCF = Cashflow.create(**param)

        return obj


# rebuild model to ensure other classes are loaded
RealEstate.model_rebuild()
