"""
Class for cashflows i.e. not relevant for income tax for example credit back payments etc.
"""
# for future importing Income due to circular import
from __future__ import annotations

from planningposition import Planningposition
from typing import TYPE_CHECKING, ClassVar, Optional, List
from pydantic import BaseModel
from monthYear import * 
from classes.scenario import *

# import Income only for typechecking due to circular import
if TYPE_CHECKING:
    from classes.income import Income

## class for aggregated free assets i.e. liqudity and assets to generate income
class Cashflow(BaseModel):
    name: str
    person: Optional[Person] = None
    planValue: Optional[List[Planningposition]] = []
    taxablePortion: Optional[float] = 0 #for capital withdrawal tax (Kapitalauszahlungssteuer)

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    liquidityRes: ClassVar[float] = 0 #liquidity Reserves
    investCapReturnRate: ClassVar[Planningposition]
    investCapIncome: ClassVar["Income"] = None # delayed assignment for Income instance due to circular import
    liquidityPlanValue: ClassVar[List[Planningposition]] = []
    investCapPlanValueStart: ClassVar[List[Planningposition]] = [] # == EndValue of previous prediod
    investCapPlanValueEnd: ClassVar[List[Planningposition]] = []

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Cashflow":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic
        return obj
