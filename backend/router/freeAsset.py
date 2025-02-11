"""
Free assets as liquidity and investments 

not for planning purposes, see AggFreeAsset
"""

from fastapi import APIRouter, HTTPException
from generalClasses import *
from utils.nameManager import *
from generalClasses.planningposition import Planningposition
from typing import ClassVar, Optional, List
from pydantic import BaseModel, field_validator
from generalClasses.monthYear import *
from router.person import * 

class FreeAsset(BaseModel):
    # Oject-attributes
    name: str
    person: Optional[Person] = None
    baseValue: float

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator('baseValue', mode='after')  
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f'{baseValue} is strict smaller than 0')
        return baseValue
    
    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "FreeAsset":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic

        return obj

    
    
#starting router    
router = APIRouter(prefix="/freeAsset", tags=["freeAsset"])

#creating a new income-object
@router.post("/create-freeAsset/")
def create_freeAsset(name: str, personName: Optional[str] = None, baseValue: Optional[float] = 0):
    try:
        new_object = FreeAsset.create(name=name, person=get_person(personName), baseValue=baseValue)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()

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



