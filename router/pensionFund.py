""" Class for PensionFund inclusive organising withdrawal as capital or pension """

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List
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

    # Surpress usage of value since we distinguish between the free attributes abovo
    def __init__(self, **data):
        super().__init__(**data)
        self.__dict__.pop("value", None)

class PensionFund(BaseModel):
    # Object-attributes
    name: str
    person: Person
    baseValue: float
    fixValue: Optional[List[Planningposition]] = [] #overturns planning value
    planValue: Optional[List[Planningposition]] = []
    savingContribution: Optional[List[Planningposition]] = [] #dt: Sparbeitrag (monthly)
    returnRate: Optional[List[Planningposition]] = []
    payout:  Optional[List[Planningposition]] = []

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    # Init-Function and adding to instanceDic
    def __init__(self, **data):
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, self.__class__.instanceDic)
        self.__class__.instanceDic[self.name] = self


#starting router
router = APIRouter(prefix="/pensionFund", tags=["pensionFund"])

#creating a new pensionFund-object
@router.post("/create-pensionFund/")
def create_pensionFund(new_object: PensionFund):
    return new_object.__class__.instanceDic[new_object.name]

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