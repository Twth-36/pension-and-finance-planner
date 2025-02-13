""" realEstates inlcusive renovations etc. """

from fastapi import APIRouter, HTTPException, Path
from typing import Optional, List
from generalClasses import *
from utils.nameManager import *
from generalClasses.planningposition import * #issue why necessary?
from pydantic import BaseModel, field_validator
from generalClasses.monthYear import *
from router.expense import *
from router.person import *
from router.scenario import *


class RealEstate(BaseModel):
    # Object-variable
    name: str
    person: Optional[Person] = None
    baseValue: Optional[float] = 0
    fixValue: Optional[List[Planningposition]] = None
    planValue: Optional[List[Planningposition]] = None

    ZIPCode: Optional[int] = None
    taxValue: Optional[List[Planningposition]] = None
    taxRate: Optional[List[Planningposition]] = None #only for dt: "Liegenschaftssteuer"

    maintCostRate: Optional[List[Planningposition]] = None
    maintenanceExpense: Optional[Expense] = None
    
    renovations: Optional[List[Planningposition]] = None
    renovationExpense: Optional[Expense] = None

    purchase: Optional[List[Planningposition]] = None
    purchaseCF: Optional[Cashflow] = None

    sale: Optional[List[Planningposition]] = None
    saleCF: Optional[Cashflow] = None

    # Class-variable
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
    def create(cls, **data) -> "RealEstate":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic
        return obj


#start router
router = APIRouter(prefix="/realEstate", tags=["realEstate"])

#creating a new income-object
@router.post("/create-realEstate/")
def create_realEstate(name: str, personName: Optional[str] = None, baseValue: Optional[float] = 0):
    try:
        new_object = RealEstate.create(name=name, person=get_person(personName), baseValue=baseValue)
        logger.debug({"New object created": new_object.name})
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()

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


