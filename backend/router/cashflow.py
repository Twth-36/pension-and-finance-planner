"""
Class for cashflows i.e. not relevant for income tax for example credit back payments etc.
"""
# for future importing Income due to circular import
from __future__ import annotations

from fastapi import APIRouter
from generalClasses import *
from generalClasses.planningposition import Planningposition
from typing import TYPE_CHECKING, ClassVar, Optional, List
from pydantic import BaseModel
from generalClasses.monthYear import * 
from router.scenario import *

# import Income only for typechecking due to circular import
if TYPE_CHECKING:
    from router.income import Income

## class for aggregated free assets i.e. liqudity and assets to generate income
class Cashflow(BaseModel):
    name: str
    person: Person
    planValue: Optional[List[Planningposition]] = []
    taxablePortion: Optional[float] = 1 #for capital withdrawal tax (Kapitalauszahlungssteuer)

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    liquidityRes: ClassVar[float] = 0 #liquidity Reserves
    investCapReturnRate: ClassVar[Planningposition]
    investCapIncome: ClassVar["Income"] = None # delayed assignment for Income instance due to circular import
    liquidityPlanValue: ClassVar[List[Planningposition]] = []
    investCapPlanValueStart: ClassVar[List[Planningposition]] = [] # == EndValue of previous prediod
    investCapPlanValueEnd: ClassVar[List[Planningposition]] = [] 


   

#starting router
router = APIRouter(prefix="/cashflow", tags=["cashflow"])

# Returns cashflow position by name
@router.get("/get-cashflow/{object_name}")
def get_cashflow(object_name: str):
    if object_name not in Cashflow.instanceDic:
        return {"Error": "object_name not found"}
    return Cashflow.instanceDic[object_name]

# Returns all cashflows
@router.get("/get-allCashflows/")
def get_allcashflows():
    return Cashflow.instanceDic

# Changes liquidity reserve
@router.put("/put-newLiquidityRes/{liquidityRes}")
def put_newLiquidityRes(liquidityRes: float):
    Cashflow.liquidityRes = liquidityRes
    return Cashflow.liquidityRes