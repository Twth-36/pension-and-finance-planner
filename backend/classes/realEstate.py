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

    baseTaxValue: Optional[float] = 0
    taxFixValue: Optional[List[Planningposition]] = []
    taxPlanValue: Optional[List[Planningposition]] = []

    taxRate: Optional[float] = 0
    taxExpense: Optional[Expense] = None

    baseImputedRentalValue: Optional[float] = 0  # dt Eigenmietwert
    imputedRentalFixValue: Optional[List[Planningposition]] = []
    imputedRentalPlanValue: Optional[List[Planningposition]] = []
    imputedRentalValueIncomeTaxPos: Optional[IncomeTaxPos] = None

    maintCostRate: float = 0
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

    @field_validator("taxExpense", mode="before")
    @classmethod
    def _load_taxExpense(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Expense.get_itemByName(v["name"])
        return v

    @field_validator("imputedRentalValueIncomeTaxPos", mode="before")
    @classmethod
    def _load_imputedRentalValueIncomeTaxPos(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return IncomeTaxPos.get_itemByName(v["name"])
        return v

    @field_validator("maintenanceExpense", mode="before")
    @classmethod
    def _load_maintenanceExpense(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Expense.get_itemByName(v["name"])
        return v

    @field_validator("renovationExpense", mode="before")
    @classmethod
    def _load_renovationExpense(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Expense.get_itemByName(v["name"])
        return v

    @field_validator("purchaseCF", mode="before")
    @classmethod
    def _load_purchaseCF(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Cashflow.get_itemByName(v["name"])
        return v

    @field_validator("saleCF", mode="before")
    @classmethod
    def _load_saleCF(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Cashflow.get_itemByName(v["name"])
        return v

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

        if obj.imputedRentalValueIncomeTaxPos is None:
            param = {"name": "Eigenmietwert: " + obj.name}
            if obj.person:
                param["person"] = obj.person
            obj.imputedRentalValueIncomeTaxPos = IncomeTaxPos.create(**param)

        return obj

    # overwrite super-function since not only planValue needs to be reset
    def reset_planValue(self, scenario: Scenario):
        # delets all planValue of an object with a specific scenario
        if not self.planValue:
            return
        super().reset_planValue(
            scenario=scenario
        )  # call super-function for resetting planValue

        # additionally reset taxValuePlanValue and imputedRentPlanValue
        self.taxPlanValue = [p for p in self.taxPlanValue if p.scenario != scenario]
        self.imputedRentalPlanValue = [
            p for p in self.imputedRentalPlanValue if p.scenario != scenario
        ]


# rebuild model to ensure other classes are loaded
RealEstate.model_rebuild()
