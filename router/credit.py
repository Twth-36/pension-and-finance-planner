""" Credit inclusive interest and backpayments"""

from fastapi import APIRouter
from typing import Optional, List, ClassVar
from generalClasses import *
from generalClasses.planningposition import * #issue why necessary?
from pydantic import BaseModel
from utils.nameManager import *
from router.expense import *
from router.scenario import *
from router.person import *

class Credit(BaseModel):
    # Object-attributes
    name: str
    person: Person
    endDate: Optional[MonthYear] = Scenario.endDate
    baseValue: Optional[float] = 0
    fixValue: Optional[List[Planningposition]] = [] #overturns planning value
    planValue: Optional[List[Planningposition]] = []
    interestRate: Optional[List[Planningposition]] = [] #p.a.
    interstExpense: Optional[Expense] = None
    realEstate: Optional[Expense] = None #if mortgage

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    # Init-Function and adding to instanceDic
    def __init__(self, **data):
        obj = super().__init__(**data)
        obj.name = generate_uniqueName(obj.name, obj.__class__.instanceDic)
        obj.__class__.instanceDic[obj.name] = obj

        return obj


#starting router
router = APIRouter(prefix="/credit", tags=["credit"])

#creating a new credit-object
@router.post("/create-credit/")
def create_credit(new_object: Credit):
    return new_object.__class__.instanceDic[new_object.name]

# Deleting an existing credit object
@router.delete("/delete-credit/{object_name}")
def delete_credit(object_name: str):
    if object_name not in Credit.instanceDic:
        return {"Error": "object_name not found"}
    
    del Credit.instanceDic[object_name]
    return {"Success": "Credit deleted"}

# Returns credit position by name
@router.get("/get-credit/{object_name}")
def get_credit(object_name: str):
    if object_name not in Credit.instanceDic:
        return {"Error": "object_name not found"}
    return Credit.instanceDic[object_name]

# Returns all Credits
@router.get("/get-allCredits/")
def get_allcredits():
    return Credit.instanceDic