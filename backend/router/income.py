""" 
Class Income for planning all possible incomes

Objects can't get created via API! see manualIncome
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List
from router.cashflow import Cashflow
from utils.nameManager import *
from generalClasses.planningposition import *
from router.person import *
from router.incomeTaxPos import *
from router.scenario import *

class Income(BaseModel):
    # Object-attributes
    name: str
    person: Optional[Person] = None
    planValue: Optional[List[Planningposition]] = [] 
    taxablePortion: Optional[float] = 1
    taxPosition: Optional[IncomeTaxPos] = None

    # Class-attribute
    instanceDic: ClassVar[dict] = {}
    cashflowPos: ClassVar[Cashflow] = None #cashlowposition on which the total flows

    #create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Income":
        #Create and validate and add to instanceDic
        obj = cls.model_validate(data)
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) 
        cls.instanceDic[obj.name] = obj

        # if incomeTaxPosition not exisiting, creating one
        if obj.taxPosition is None:
            obj.taxPosition = IncomeTaxPos.create(name=obj.name, person=obj.person)

        return obj








#starting router
router = APIRouter(prefix="/income", tags=["income"])

# Returns income position by name
@router.get("/get-income/{object_name}")
def get_income(object_name: str):
    if object_name not in Income.instanceDic:
        return {"Error": "object_name not found"}
    return Income.instanceDic[object_name]

# Returns all Incomes
@router.get("/get-allincomes/")
def get_allincomes():
    return Income.instanceDic
