"""
Class Expense for planning all possible expenses

Objects can't get created via API! see manualExpense
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
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
    
    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Expense":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic

        # if incomeTaxPosition not exisiting, creating one
        if obj.taxPosition is None:
            obj.taxPosition = IncomeTaxPos.create(name=obj.name)

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

