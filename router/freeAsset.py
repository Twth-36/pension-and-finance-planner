""" Free assets as liquidity and investments """

from fastapi import APIRouter
from generalClasses import *
from generalClasses.planningposition import Planningposition
from typing import Optional, List
from pydantic import BaseModel
from generalClasses.monthYear import * 

## class for all freeAsset in detail
class FreeAsset(BaseModel):
    name: str
    person_id: int
    baseValue: float

## class for aggregated free assets i.e. liqudity and assets to generate income
class MainFreeAsset(BaseModel):
    name: str
    person_id: int
    planValue: Optional[List[Planningposition]] = []
    returnRate: Optional[List[Planningposition]] = []

# Dictionary to manage all FreeAsset-objects
freeAssetDic = {}

# Dictionary to mana MainFreeAsset-objects
mainFreeAssetDic = {
    0: {
        "name": "Liquidität",
        "person_id": 2,
        "planValue": []
    },
    1: {
        "name": "Kapital zur Einkommensgewinnung",
        "person_id": 2,
        "planValue": []
    }
}

router = APIRouter()

#creating a new freeAsset-object
@router.post("/freeAsset/create-freeAsset/{freeAsset_id}")
def create_freeAsset(freeAsset_id: int, freeAsset: FreeAsset):
    if freeAsset_id in freeAssetDic:
        return {"Error": "freeAsset_id already used"}
    
    freeAssetDic[freeAsset_id] = freeAsset
    return freeAssetDic[freeAsset_id]

#changes on existing freeAsset-object
@router.put("/freeAsset/update-freeAsset/{freeAsset_id}")
def update_freeAsset(freeAsset_id: int, freeAsset: FreeAsset):
    if freeAsset_id not in freeAssetDic:
        return {"Error": "freeAsset_id not found"}

    freeAssetDic[freeAsset_id].update(freeAsset)
    return freeAssetDic[freeAsset_id]

# Deleting an existing freeAsset-object
@router.delete("/freeAsset/delete-freeAsset/{freeAsset_id}")
def delete_freeAsset(freeAsset_id: int):
    if freeAsset_id not in freeAssetDic:
        return {"Error": "freeAsset_id not found"}
    
    del freeAssetDic[freeAsset_id]
    return {"Success": "FreeAsset deleted"}

# Returns freeAsset position by id
@router.get("/freeAsset/get-freeAsset/{freeAsset_id}")
def get_freeAsset(freeAsset_id: int):
    if freeAsset_id not in freeAssetDic:
        return {"Error": "freeAsset_id not found"}
    return freeAssetDic[freeAsset_id]

# Returns all freeAssets
@router.get("/freeAsset/get-allfreeAssets/")
def get_allfreeAssets():
    return freeAssetDic

# Returns first free id in freeAssetDic
@router.get("/freeAsset/get-firstFreeId/")
def get_firstFreeId():
    free_id = 0
    while free_id in freeAssetDic:
        free_id += 1
    return free_id















## ExampleValues for show-purposes and testing
freeAsset = FreeAsset(name="MigrosBank Sparkonto", person_id=0, baseValue=50000)
create_freeAsset(get_firstFreeId(), freeAsset)

freeAsset = FreeAsset(name="Raiffeisen Sparkonto", person_id=1, baseValue=75000)
create_freeAsset(get_firstFreeId(), freeAsset)