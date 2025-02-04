""" Free assets as liquidity and investments """
from fastapi import APIRouter, Path
from .planningposition import *
from typing import Optional


class FreeAsset(Planningposition):
    returnRate: Optional[float]=0

freeAssetDic = {}

router = APIRouter()

#creating a new free-asset-object
@router.post("/freeAsset/create-freeAsset/{freeAsset_id}")
def create_freeAsset(freeAsset_id: int, freeAsset: FreeAsset):
    if freeAsset_id in freeAssetDic:
        return {"Error": "freeAsset_id already used"}
    
    freeAssetDic[freeAsset_id] = freeAsset
    return freeAssetDic[freeAsset_id]

#changes on existing free-asset-object
@router.put("/freeAsset/update-freeAsset/{freeAsset_id}")
def update_freeAsset(freeAsset_id: int, freeAsset: FreeAsset):
    if freeAsset_id not in freeAssetDic:
        return {"Error": "freeAsset_id not found"}
    freeAssetDic[freeAsset_id].update(freeAsset)
    return freeAssetDic[freeAsset_id]