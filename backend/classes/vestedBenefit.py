"""Class for organising vestedBenefits (Freizügigkeitsguthaben)"""

from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List
from .planningposition import *
from .expense import *


class VestedBenefit(Planningobject):
    # Object-Variables
    baseValue: Optional[float] = 0
    returnRate: Optional[float] = 0
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
    def create(cls, **data) -> "VestedBenefit":
        obj = super().create(**data)  # Creation in Planningobjectclass

        if obj.payoutCF is None:
            param = {"name": "Auszahlung: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.payoutCF = Cashflow.create(**param)

        return obj

    @classmethod
    def copy_toNewScenario(cls, new_scenario: Scenario, src_scenario: Scenario):
        for obj in cls.instanceDic.values():

            # all lists with planValue where the scenario needs to be dublicated
            lists = [obj.planValue, obj.payoutDate]

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
VestedBenefit.model_rebuild()
