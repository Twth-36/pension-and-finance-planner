"""
Free assets as liquidity and investments 

not for planning purposes, see AggFreeAsset
"""

from fastapi import APIRouter
from generalClasses import *
from generalClasses.nameManager import *
from generalClasses.planningposition import Planningposition
from typing import ClassVar, Optional, List
from pydantic import BaseModel
from generalClasses.monthYear import * 

class FreeAsset(BaseModel):
    # Oject-attributes
    name: str
    person_id: int
    baseValue: float

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    # Init-Function and adding to instanceDic
    def __init__(self, **data):
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, self.__class__.instanceDic)
        self.__class__.instanceDic[self.name] = self
    
#starting router    
router = APIRouter(prefix="/freeAsset", tags=["freeAsset"])

#creating a new freeAsset-object
@router.post("/create-freeAsset/")
def create_freeAsset(new_object: FreeAsset):
    return new_object.__class__.instanceDic[new_object.name]

# Deleting an existing freeAsset object
@router.delete("/delete-freeAsset/{object_name}")
def delete_freeAsset(object_name: str):
    if object_name not in FreeAsset.instanceDic:
        return {"Error": "object_name not found"}
    
    del FreeAsset.instanceDic[object_name]
    return {"Success": "freeAsset deleted"}

# Returns freeAsset position by name
@router.get("/get-freeAsset/{object_name}")
def get_freeAsset(object_name: str):
    if object_name not in FreeAsset.instanceDic:
        return {"Error": "object_name not found"}
    return FreeAsset.instanceDic[object_name]

# Returns all freeAssets
@router.get("/get-allFreeAssets/")
def get_allfreeAssets():
    return FreeAsset.instanceDic



