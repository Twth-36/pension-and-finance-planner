"""
Class Expense for planning all possible expenses

Objects can't get created via API! see manualExpense
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses.planningposition import *
from router.incomeTaxPos import *
from router.person import *


class Expense(BaseModel):
    # Object-attributes
    name: str
    person: Person
    planValue: Optional[List[Planningposition]] = []
    taxablePortion: Optional[List[Planningposition]] = []
    inflationRate: Optional[List[Planningposition]] = []
    taxPosition: IncomeTaxPos

    # Class-attribute
    instanceDic: ClassVar[dict] = {}

    #Init-Function and adding to instanceDic
    def __init__(self, **data):
        """
        not using self.__class__ sinc if the object gets created by another class which inherits from this one, 
        self.__class__ refers on the class the object gets actually created
        """
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, Expense.instanceDic)
        Expense.instanceDic[self.name] = self


#starting router
router = APIRouter(prefix="/expense", tags=["expense"])

# Returns expense position by name
@router.get("/get-expense/{object_name}")
def get_expense(object_name: str):
    if object_name not in Expense.instanceDic:
        return {"Error": "object_name not found"}
    return Expense.instanceDic[object_name]

# Returns all Expenses
@router.get("/get-allexpenses/")
def get_allexpenses():
    return Expense.instanceDic

