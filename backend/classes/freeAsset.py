"""
Free assets as liquidity and investments

not for planning purposes, see AggFreeAsset
"""

from backend.classes.income import Income
from backend.classes.planningobject import Planningobject
from backend.utils.nameManager import *
from .planningposition import *
from typing import ClassVar, Optional, List
from pydantic import BaseModel, field_validator
from ..utils.monthYear import *
from .person import *


class FreeAsset(Planningobject):
    # Oject-attributes
    baseValue: Optional[float] = 0

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    liqRes: ClassVar[Optional[float]] = 0  # liquidity Reserves
    planValueLiq: ClassVar[Optional[List[Planningposition]]] = (
        []
    )  # positions for aggregated free Assets
    planValueInvestCap: ClassVar[Optional[List[Planningposition]]] = []
    returnRateInvestCap: ClassVar[Optional[float]] = 0

    returnIncome: ClassVar[Optional[Income]] = None

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} is strict smaller than 0")
        return baseValue

    # overwrite super-function since not planValue needs to be reset
    @classmethod
    def reset_allPlanValue(cls, scenario: Scenario):
        # reset planValue of invested Capital and liquidity
        cls.planValueLiq = [p for p in cls.planValueLiq if p.scenario != scenario]
        cls.planValueInvestCap = [
            p for p in cls.planValueInvestCap if p.scenario != scenario
        ]

    @classmethod
    def reset_planValue(cls, period: MonthYear, scenario: Scenario):
        # reset planValue of invested Capital and liquidity in one period
        cls.planValueLiq = [
            p
            for p in cls.planValueLiq
            if (p.scenario != scenario or p.period != period)
        ]
        cls.planValueInvestCap = [
            p
            for p in cls.planValueInvestCap
            if (p.scenario != scenario or p.period != period)
        ]


# rebuild model to ensure other classes are loaded
FreeAsset.model_rebuild()
FreeAsset.returnIncome = Income.create(name="Einkommen aus Kapital", taxablePortion=50)
