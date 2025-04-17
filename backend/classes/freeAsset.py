"""
Free assets as liquidity and investments

not for planning purposes, see AggFreeAsset
"""

from backend.utils.nameManager import *
from .planningposition import *
from typing import ClassVar, Optional, List
from pydantic import BaseModel, field_validator
from .monthYear import *
from .person import *


class FreeAsset(BaseModel):
    # Oject-attributes
    name: str
    baseValue: Optional[float] = 0
    person: Optional[Person] = None

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    liqRes: ClassVar[Optional[float]] = 0  # liquidity Reserves
    planValueLiq: ClassVar[Optional[List[Planningposition]]] = (
        []
    )  # positions for aggregated free Assets
    planValueInvestCap: ClassVar[Optional[List[Planningposition]]] = []
    returnRateInvestCap: ClassVar[Optional[float]] = 0

    # Validation for unique name
    @field_validator("name", mode="after")
    @classmethod
    def check_uniquename(cls, name: str) -> str:
        if name == "":
            raise ValueError(f"May not be empty")
        if name in cls.instanceDic:
            raise ValueError(f"An object with name '{name}' already exists")
        return name

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} is strict smaller than 0")
        return baseValue

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "FreeAsset":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic
        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "FreeAsset":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        # check first if objects is still used anywhere
        ##TODO
        del self.__class__.instanceDic[self.name]


# rebuild model to ensure other classes are loaded
FreeAsset.model_rebuild()
