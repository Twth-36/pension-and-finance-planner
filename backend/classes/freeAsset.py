"""
Free assets as liquidity and investments

not for planning purposes, see AggFreeAsset
"""

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

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} is strict smaller than 0")
        return baseValue


# rebuild model to ensure other classes are loaded
FreeAsset.model_rebuild()
