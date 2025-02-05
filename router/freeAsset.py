""" Free assets as liquidity and investments """

from fastapi import APIRouter, Path
from generalClasses import *
from generalClasses.planningposition import Planningposition
from typing import Optional, List, Dict
from pydantic import BaseModel


class FreeAsset(BaseModel):
    name: str
    person_id: int
    currentValue: List[Planningposition]
    returnRate: List[Planningposition]
  

freeAssetDic: Dict[int, FreeAsset] = {}

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