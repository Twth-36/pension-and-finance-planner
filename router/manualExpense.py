""" Class ManualExpense for planning all possible expenses, which do not depend on another object (unlike mortgagepayments, taxes etc.)"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses.planningposition import *
from router.expense import *
from router.incomeTaxPos import *
from router.person import *


class ManualExpense(Expense):
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
router = APIRouter(prefix="/expense", tags=["expense"])

#creating a new income-object
@router.post("/create-manualExpense/")
def create_manualExpense(new_object: ManualExpense):
    return new_object.__class__.instanceDic[new_object.name]

# Returns all manualExpenses
@router.get("/get-manualExpenses/")
def get_manualExpenses():
    return ManualExpense.instanceDic

