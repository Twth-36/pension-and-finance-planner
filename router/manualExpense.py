""" Class ManualExpense for planning all possible expenses, which do not depend on another object (unlike mortgagepayments, taxes etc.)"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses.planningposition import *
from router.expense import *
from router.incomeTaxPos import *
from router.person import *


class ManualExpense(Expense):
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
            raise ValueError(f'baseValue: {baseValue} may not be negative')
        return baseValue 

#starting router
router = APIRouter(prefix="/manualExpense", tags=["manualExpense"])

#creating a new manualExpense-object
@router.post("/create-manualExpense/")
def create_manualExpense(name: str, personName: Optional[str] = None, baseValue: Optional[float] = 0):
    try:
        new_object = ManualExpense.create(name=name, person=get_person(personName), baseValue=baseValue)
        logger.debug({"New object created": new_object.name})
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()

# Returns all manualExpenses
@router.get("/get-manualExpenses/")
def get_manualExpenses():
    return ManualExpense.instanceDic

