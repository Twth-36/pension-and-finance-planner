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
    depositAutomatic: Optional[List[Planningposition]] = []
    depositExpense: Optional[Expense] = (
        None  # expense Position where deposits are accounted
    )

    WEF: Optional[List[Planningposition]] = []
    WEFCF: Optional[Cashflow] = None

    payoutDate: Optional[List[Planningposition]] = (
        []
    )  # Value not used (only scenario and month)
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

    @field_validator("WEFCF", mode="before")
    @classmethod
    def _load_WEFCF(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Cashflow.get_itemByName(v["name"])
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

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Pillar3a":
        obj = super().create(**data)  # Creation in Planningobjectclass

        if obj.depositExpense is None:
            param = {"name": "Einzahlung: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.depositExpense = Expense.create(**param)

        if obj.WEFCF is None:
            param = {"name": "WEF: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.WEFCF = Cashflow.create(**param)

        if obj.payoutCF is None:
            param = {"name": "Auszahlung: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.payoutCF = Cashflow.create(**param)

        return obj

    # overwrite super-function since not only planValue needs to be reset
    def reset_planValue(self, scenario: Scenario):
        # delets all planValue of an object with a specific scenario
        if not self.planValue:
            return
        super().reset_planValue(
            scenario=scenario
        )  # call super-function for resetting planValue

        # additionally reset depositAutomatic
        self.depositAutomatic = [
            p for p in self.depositAutomatic if p.scenario != scenario
        ]

    @classmethod
    def copy_toNewScenario(cls, new_scenario: Scenario, src_scenario: Scenario):
        for obj in cls.instanceDic.values():

            # all lists with planValue where the scenario needs to be dublicated
            lists = [
                obj.planValue,
                obj.deposit,
                obj.depositAutomatic,
                obj.WEF,
                obj.payoutDate,
            ]

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
Pillar3a.model_rebuild()
