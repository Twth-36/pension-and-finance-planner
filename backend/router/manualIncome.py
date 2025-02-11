""" Class ManualIncome for planning all possible incomes, which do not depend on another object (unlike pension etc.)"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from generalClasses.planningposition import *
from router.income import *
from router.incomeTaxPos import *
from router.person import *


class ManualIncome(Income):
    # Object-attributes
    baseValue: Optional[float] = 0 #p.a.
    fixValue: Optional[List[Planningposition]] = [] #overturns planning value

    # Class-attribute
    instanceDic: ClassVar[dict] = {}


    # Validation non-negative baseValue
    @field_validator('baseValue', mode='after')  
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f'{baseValue} is strict smaller than 0')
        return baseValue
    


#starting router
router = APIRouter(prefix="/manualIncome", tags=["manualIncome"])

#creating a new income-object
@router.post("/create-manualIncome/")
def create_manualIncome(name: str, personName: str, baseValue: Optional[float] = 0):
    try:
        new_object = ManualIncome.create(name=name, person=get_person(personName), baseValue=baseValue)
        logger.debug({"New object created": new_object.name})
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()

# Returns all manualIncomes
@router.get("/get-manualIncomes/")
def get_manualIncomes():
    return ManualIncome.instanceDic

