""" Class for PensionFund inclusive organising withdrawal as capital or pension """

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import ClassVar, Optional, List
from router.expense import *
from router.income import *
from utils.nameManager import *
from generalClasses.planningposition import *
from router.person import *


class PensFundPayoutPos(Planningposition):
    # extends Planningposition with more variable
    """
    Inherited attributes:
        scenario: Scenario
        period: MonthYear
        value: Optional[float] = 0
        inDoc: Optional[bool] = False
        description: Optional[str] = None
    """
    withdrawalPortion: float # Portion which gets withdrawed as part of a (partly-)Pension
    capitalPortion: float # Portion OF THE WITHDRAWED pensioncapital which gets paid out as capital
    conversionRate: float # dt: Umwandlungssatz

class PensionFund(BaseModel):
    # Object-attributes
    name: str
    person: Person
    baseValue: float
    fixValue: Optional[List[Planningposition]] = [] #overturns planning value
    planValue: Optional[List[Planningposition]] = []
    returnRate: Optional[List[Planningposition]] = []
    savingContribution: Optional[List[Planningposition]] = [] #dt: Sparbeitrag (monthly)
    
    buyin: Optional[List[Planningposition]] = []
    buyinExpense: Optional[Expense] = None #Expenseobject to make buyins
    
    payout:  Optional[List[Planningposition]] = []
    pensionIncome: Optional[Income] = None

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
    def create(cls, **data) -> "PensionFund":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic

        #if no pensionIncome-object is assigned -> generate one
        if obj.pensionIncome is None:
            obj.pensionIncome = Income.create(name="Rente - " + obj.name, person=obj.person, taxablePortion=1)
        
        return obj
    




#starting router
router = APIRouter(prefix="/pensionFund", tags=["pensionFund"])

#creating a new income-object
@router.post("/create-pensionFund/")
def create_pensionFund(name: str, personName: str, baseValue: Optional[float] = 0):
    try:
        new_object = PensionFund.create(name=name, person=get_person(personName), baseValue=baseValue)
        logger.debug({"New object created": new_object.name})
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()

# Deleting an existing pensionFund object
@router.delete("/delete-pensionFund/{object_name}")
def delete_pensionFund(object_name: str):
    if object_name not in PensionFund.instanceDic:
        return {"Error": "object_name not found"}
    
    del PensionFund.instanceDic[object_name]
    return {"Success": "PensionFund deleted"}

# Returns pensionFund position by name
@router.get("/get-pensionFund/{object_name}")
def get_pensionFund(object_name: str):
    if object_name not in PensionFund.instanceDic:
        return {"Error": "object_name not found"}
    return PensionFund.instanceDic[object_name]

# Returns all PensionFunds
@router.get("/get-allpensionFunds/")
def get_allpensionFunds():
    return PensionFund.instanceDic