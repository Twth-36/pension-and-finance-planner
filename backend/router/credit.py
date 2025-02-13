""" Credit inclusive interest and backpayments"""

from fastapi import APIRouter, HTTPException
from typing import Optional, List, ClassVar
from generalClasses import *
from generalClasses.planningposition import * #issue why necessary?
from pydantic import BaseModel, field_validator
from utils.nameManager import *
from router.expense import *
from router.scenario import *
from router.person import *

class Credit(BaseModel):
    # Object-attributes
    name: str
    person: Optional[Person] = None
    endDate: Optional[MonthYear] = Scenario.endDate
    baseValue: Optional[float] = 0
    planValue: Optional[List[Planningposition]] = []

    interestRate: Optional[List[Planningposition]] = [] #p.a.
    interstExpense: Optional[Expense] = None
    
    payback: Optional[List[Planningposition]] = []
    paybackCF: Optional[Cashflow] = None

    increase: Optional[List[Planningposition]] = []
    increaseCF: Optional[Cashflow] = None

    realEstate: Optional[Expense] = None #if mortgage

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    @field_validator('baseValue', mode='after')  
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f'{baseValue} may not be negative')
        return baseValue 
    
    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Credit":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic
        return obj


#starting router
router = APIRouter(prefix="/credit", tags=["credit"])

#creating a new cedit-object
@router.post("/create-credit/")
def create_credit(name: str, personName: Optional[str] = None, baseValue: Optional[float] = 0):
    try:
        new_object = Credit.create(name=name, person=get_person(personName), baseValue=baseValue)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()
