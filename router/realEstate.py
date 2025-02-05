""" realEstates inlcusive renovations etc. """

from fastapi import APIRouter, Path
from typing import Optional, List
from generalClasses import *
from generalClasses.planningposition import * #issue why necessary?
from pydantic import BaseModel


class RealEstate(BaseModel):
    value: List[Planningposition]
    taxValue: List[Planningposition]
    realEstateTaxRate: List[Planningposition]
    maintenanceCostRate: float
    renovationExpense_id: Optional[int] = None

realEstateDic = {}


router = APIRouter()

#creating a new realEstate-object
@router.post("/realEstate/create-realEstate/{realEstate_id}")
def create_realEstate(realEstate_id: int, realEstate: RealEstate):
    if realEstate_id in realEstateDic:
        return {"Error": "realEstate_id already used"}
    
    realEstateDic[realEstate_id] = realEstate
    return realEstateDic[realEstate_id]

# Changes on existing realEstate-object
@router.put("/realEstate/update-realEstate/{realEstate_id}")
def update_realEstate(realEstate_id: int, realEstate: RealEstate):
    if realEstate_id not in realEstateDic:
        return {"Error": "realEstate_id not found"}
    
    realEstateDic[realEstate_id].update(realEstate)
    return realEstateDic[realEstate_id]

# Deleting an existing realEstate object
@router.delete("/realEstate/delete-realEstate/{realEstate_id}")
def delete_realEstate(realEstate_id: int):
    if realEstate_id not in realEstateDic:
        return {"Error": "realEstate_id not found"}
    
    del realEstateDic[realEstate_id]
    return {"Success": "realEstate deleted"}

# Returns realEstate position by id
@router.get("/realEstate/get-realEstate/{realEstate_id}")
def get_realEstate(realEstate_id: int):
    if realEstate_id not in realEstateDic:
        return {"Error": "realEstate_id not found"}
    return realEstateDic[realEstate_id]

# Returns all realEstates
@router.get("/realEstate/get-allrealEstates/")
def get_allrealEstates():
    return realEstateDic

