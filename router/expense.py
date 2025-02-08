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
        not using obj.__class__ since if the object gets created by another class which inherits from this one, 
        obj.__class__ refers on the class the object gets actually created
        """
        obj = super().__init__(**data)
        obj.name = generate_uniqueName(obj.name, Expense.instanceDic)
        Expense.instanceDic[obj.name] = obj

        return obj


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

