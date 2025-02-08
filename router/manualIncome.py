""" Class ManualIncome for planning all possible incomes, which do not depend on another object (unlike pension etc.)"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
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

    #Init-Function and adding to instanceDic
    def __init__(self, **data):
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, self.__class__.instanceDic)
        self.__class__.instanceDic[self.name] = self


#starting router
router = APIRouter(prefix="/manualIncome", tags=["manualIncome"])

#creating a new income-object
@router.post("/create-manualIncome/")
def create_manualIncome(name: str, personName: str, baseValue: Optional[float] = 0):
    new_object = ManualIncome(name=name, person=get_person(personName), baseValue=baseValue)
    return new_object

# Returns all manualIncomes
@router.get("/get-manualIncomes/")
def get_manualIncomes():
    return ManualIncome.instanceDic

