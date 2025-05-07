"""Credit inclusive interest and backpayments"""

from typing import Optional, List, ClassVar
from pydantic import BaseModel, field_validator

from backend.classes.realEstate import *
from .expense import *
from .scenario import *
from .person import *
from ..utils.monthYear import *
from .planningposition import *


class Credit(Planningobject):
    # Object-attributes
    endDate: Optional[MonthYear] = None
    baseValue: Optional[float] = 0
    baseInterestRate: Optional[float] = 0

    interestRate: Optional[List[Planningposition]] = []  # p.a.
    interestExpense: Optional[Expense] = None

    payback: Optional[List[Planningposition]] = []
    paybackCF: Optional[Cashflow] = None

    increase: Optional[List[Planningposition]] = []
    increaseCF: Optional[Cashflow] = None

    realEstate: Optional[RealEstate] = None  # if mortgage

    # Class-attribute
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} may not be negative")
        return baseValue

    @field_validator("interestExpense", mode="before")
    @classmethod
    def _load_interestExpense(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Expense.get_itemByName(v["name"])
        return v

    @field_validator("paybackCF", mode="before")
    @classmethod
    def _load_paybackCF(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Cashflow.get_itemByName(v["name"])
        return v

    @field_validator("increaseCF", mode="before")
    @classmethod
    def _load_increaseCF(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Cashflow.get_itemByName(v["name"])
        return v

    @field_validator("realEstate", mode="before")
    @classmethod
    def _load_realEstate(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return RealEstate.get_itemByName(v["name"])
        return v

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Credit":

        obj = super().create(**data)

        if obj.interestExpense is None:
            param = {"name": "Zinszahlung: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.interestExpense = Expense.create(**param)

        if obj.increaseCF is None:
            param = {"name": "Krediterhöhung: " + obj.name}
            if obj.person:
                param["person"] = obj.person
            obj.increaseCF = Cashflow.create(**param)

        if obj.paybackCF is None:
            param = {"name": "Amortisation: " + obj.name}
            if obj.person:
                param["person"] = obj.person
            obj.paybackCF = Cashflow.create(**param)

        return obj

    @classmethod
    def copy_toNewScenario(cls, new_scenario: Scenario, src_scenario: Scenario):

        for obj in cls.instanceDic.values():
            # all lists with planValue where the scenario needs to be dublicated
            lists = [obj.planValue, obj.interestRate, obj.payback, obj.increase]

            # duplicates all scenario related fields to a newscenario
            for planPosList in lists:
                for pos in planPosList:
                    if pos.scenario == src_scenario:
                        Planningposition(
                            scenario=new_scenario,
                            period=pos.period,
                            value=pos.value,
                            inDoc=pos.inDoc,
                            description=pos.description,
                        ).add_toList(planPosList)


# rebuild model to ensure other classes are loaded
Credit.model_rebuild()
