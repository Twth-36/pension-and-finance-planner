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
    person: Optional[Person] = None
    baseValue: float

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    liquidityRes: ClassVar[float] = 0 #liquidity Reserves
    planValueLiq: ClassVar[Optional[List[Planningposition]]] = [] #positions for aggregated free Assets
    planValueInvestCap: ClassVar[Optional[List[Planningposition]]] = []
    returnRateInvestCap: Optional[float] = 0

    # validation config
    model_config = ConfigDict(revalidate_instances='always')

    # Validation for unique name
    @field_validator("name", mode="after")  
    @classmethod
    def check_uniquename(cls, name: str) -> str:
        if name == "": raise ValueError(f"May not be empty")
        if name in cls.instanceDic:
            raise ValueError(f"An object with name '{name}' already exists")
        return name

    # Validation non-negative baseValue
    @field_validator('baseValue', mode='before')  
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f'{baseValue} is strict smaller than 0')
        return baseValue
    
    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "FreeAsset":
        obj = cls.model_validate(data) #Creation and validation
        cls.instanceDic[obj.name] = obj #adding to instanceDic

        return obj
    
    @classmethod
    def get_itemByName(cls, name: str) -> "FreeAsset":
        return cls.instanceDic[name]
    
    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname


