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


# rebuild model to ensure other classes are loaded
VestedBenefit.model_rebuild()
