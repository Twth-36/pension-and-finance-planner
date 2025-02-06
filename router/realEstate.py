""" realEstates inlcusive renovations etc. """

from fastapi import APIRouter, Path
from typing import Optional, List
from generalClasses import *
from generalClasses.planningposition import * #issue why necessary?
from pydantic import BaseModel
from generalClasses.monthYear import *
from router.scenario import *


class RealEstate(BaseModel):
    name: str
    person_id: int
    baseValue: float
    ZIPCode: Optional[int]
    fixValue: Optional[List[Planningposition]] = None
    planValue: Optional[List[Planningposition]] = None
    taxValue: Optional[List[Planningposition]] = None
    realEstateTaxRate: Optional[List[Planningposition]] = None
    maintenanceCostRate: Optional[List[Planningposition]] = None
    maintenanceExpense_id: Optional[int] = None
    renovations: Optional[List[Planningposition]] = None
    renovationExpense_id: Optional[int] = None

realEstateDic = {}


router = APIRouter(prefix="/realEstate", tags=["realEstate"])

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

# Returns first free id in realEstateDic
@router.get("/realEstate/get-firstFreeId/")
def get_firstFreeId():
    free_id = 0
    while free_id in realEstateDic:
        free_id += 1
    return free_id










## ExampleValues for show-purposes and testing
freeAsset = RealEstate(name="EFH Biel", person_id=2, baseValue=750000, ZIPCode=2502)
create_realEstate(get_firstFreeId(), freeAsset)
