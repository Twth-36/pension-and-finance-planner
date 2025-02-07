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
    fixValue: Optional[List[Planningposition]] = []

    # Class-attribute
    instanceDic: ClassVar[dict] = {}

    #Init-Function and adding to instanceDic
    def __init__(self, **data):
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, self.__class__.instanceDic)
        self.__class__.instanceDic[self.name] = self


#starting router
router = APIRouter(prefix="/income", tags=["income"])

#creating a new income-object
@router.post("/create-manualIncomeTaxPosition/")
def create_manualIncomeTaxPosition(new_object: ManualIncome):
    return new_object.__class__.instanceDic[new_object.name]

# Returns all manualIncomeTaxPositions
@router.get("/get-manualIncomeTaxPositions/")
def get_manualIncomeTaxPositions():
    return ManualIncome.instanceDic

