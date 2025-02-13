""" Class for organising pillar 3a """

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List
from utils.nameManager import *
from generalClasses.planningposition import *
from enum import Enum
from router.expense import *

class Pillar3a(BaseModel):
    # Object-Variables
    name: str
    person: Person
    baseValue: Optional[float] = 0
    planValue: Optional[List[Planningposition]] = []
    returnRate: Optional[List[Planningposition]] = []
    depositExpense: Optional[Expense] = None # expense Position where deposits are accounted
    payoutCFpos: Optional[Cashflow] = None

    #Class-variables
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
    def create(cls, **data) -> "Pillar3a":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic

        return obj

#Special class for Pillar3a Insurances 
class Pillar3aInsurance(Pillar3a):
    fixDeposit: Optional[float] = 0 # p.a.
    endDate: Optional[MonthYear] = None
    endValue: Optional[float] = None # fixed "Erlebensfallkapital"
    fixValue: Optional[List[Planningposition]] = [] #overturns planning value

    #Class-variables
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator('baseValue', mode='after')  
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f'{baseValue} is strict smaller than 0')
        return baseValue 
    
    
    

#starting router
router = APIRouter(prefix="/pillar3a", tags=["pillar3a"])

#creating a new pillar3a-object
@router.post("/create-pillar3a/")
def create_pillar3a(name: str, personName: str, baseValue: Optional[float] = 0):
    try:
        new_object = Pillar3a.create(name=name, person=get_person(personName), baseValue=baseValue)
        logger.debug({"New object created": new_object.name})
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()

#creating a new pillar3a-object
@router.post("/create-pillar3aInsurance/")
def create_pillar3aInsurance(name: str, personName: str, baseValue: Optional[float] = 0):
    try:
        new_object = Pillar3aInsurance.create(name=name, person=get_person(personName), baseValue=baseValue)
        logger.debug({"New object created": new_object.name})
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()

# Deleting an existing pillar3a object
@router.delete("/delete-pillar3a/{object_name}")
def delete_pillar3a(object_name: str):
    if object_name not in Pillar3a.instanceDic:
        return {"Error": "object_name not found"}
    
    del Pillar3a.instanceDic[object_name]
    return {"Success": "Pillar3a deleted"}

# Returns pillar3a position by name
@router.get("/get-pillar3a/{object_name}")
def get_pillar3a(object_name: str):
    if object_name not in Pillar3a.instanceDic:
        return {"Error": "object_name not found"}
    return Pillar3a.instanceDic[object_name]

# Returns all Pillar3as
@router.get("/get-allPillar3as/")
def get_allpillar3as():
    return Pillar3a.instanceDic

# Returns all Pillar3as
@router.get("/get-allPillar3aInsurances/")
def get_allpillar3aInsurances():
    return Pillar3aInsurance.instanceDic

