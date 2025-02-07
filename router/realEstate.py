""" realEstates inlcusive renovations etc. """

from fastapi import APIRouter, Path
from typing import Optional, List
from generalClasses import *
from generalClasses.nameManager import *
from generalClasses.planningposition import * #issue why necessary?
from pydantic import BaseModel
from generalClasses.monthYear import *
from router.scenario import *


class RealEstate(BaseModel):
    # Object-variable
    name: str
    person_id: int
    baseValue: float
    ZIPCode: Optional[int]
    fixValue: Optional[List[Planningposition]] = None
    planValue: Optional[List[Planningposition]] = None
    taxValue: Optional[List[Planningposition]] = None
    realEstateTaxRate: Optional[List[Planningposition]] = None #only for dt: "Liegenschaftssteuer"
    maintenanceCostRate: Optional[List[Planningposition]] = None
    maintenanceExpense_id: Optional[int] = None
    renovations: Optional[List[Planningposition]] = None
    renovationExpense_id: Optional[int] = None

    # Class-variable
    instanceDic: ClassVar[dict] = {}

    # Init-Function and adding to instanceDic
    def __init__(self, **data):
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, self.__class__.instanceDic)
        self.__class__.instanceDic[self.name] = self

#start router
router = APIRouter(prefix="/realEstate", tags=["realEstate"])

#creating a new realEstate-object
@router.post("/create-realEstate/")
def create_realEstate(new_object: RealEstate):
    return new_object.__class__.instanceDic[new_object.name]

# Deleting an existing realEstate object
@router.delete("/delete-realEstate/{object_name}")
def delete_realEstate(object_name: str):
    if object_name not in RealEstate.instanceDic:
        return {"Error": "object_name not found"}
    
    del RealEstate.instanceDic[object_name]
    return {"Success": "RealEstate deleted"}

# Returns realEstate position by name
@router.get("/get-realEstate/{object_name}")
def get_realEstate(object_name: str):
    if object_name not in RealEstate.instanceDic:
        return {"Error": "object_name not found"}
    return RealEstate.instanceDic[object_name]

# Returns all RealEstates
@router.get("/get-allRealEstates/")
def get_allrealEstates():
    return RealEstate.instanceDic


