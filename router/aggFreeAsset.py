"""
Class for the aggregated free assets which is used for planning purposes

objects are fixed and should not be created
"""

from fastapi import APIRouter
from generalClasses import *
from generalClasses.planningposition import Planningposition
from typing import ClassVar, Optional, List
from pydantic import BaseModel, validator
from generalClasses.monthYear import * 


## class for aggregated free assets i.e. liqudity and assets to generate income
class AggFreeAsset(BaseModel):
    name: str
    person_id: int
    planValue: Optional[List[Planningposition]] = []
    returnRate: Optional[List[Planningposition]] = []

    # Class-attributes
    liquidityRes: ClassVar[float] = 0 #liquidity Reserves
    instanceDic: ClassVar[dict] = {
        "Liquidität": {
            "name": "Liquidität",
            "person_id": 2,
            "planValue": []
        },
        "Kapital zur Einkommensgewinnung": {
            "name": "Kapital zur Einkommensgewinnung",
            "person_id": 2,
            "planValue": []
        }
    }

    
 

#starting router
router = APIRouter(prefix="/aggFreeAsset", tags=["aggFreeAsset"])

# Returns aggFreeAsset position by name
@router.get("/get-aggFreeAsset/{object_name}")
def get_aggFreeAsset(object_name: str):
    if object_name not in AggFreeAsset.instanceDic:
        return {"Error": "object_name not found"}
    return AggFreeAsset.instanceDic[object_name]

# Returns all aggFreeAssets
@router.get("/get-allAggFreeAssets/")
def get_allaggFreeAssets():
    return AggFreeAsset.instanceDic

# Changes liquidity reserve
@router.put("/put-newLiquidityRes/{liquidityRes}")
def put_newLiquidityRes(liquidityRes: float):
    AggFreeAsset.liquidityRes = liquidityRes
    return AggFreeAsset.liquidityRes