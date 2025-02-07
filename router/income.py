""" 
Class Income for planning all possible incomes

Objects can't get created via API! see manualIncome
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List
from generalClasses.nameManager import *
from generalClasses.planningposition import *

class Income(BaseModel):
    # Object-attributes
    name: str
    person_id: int
    planValue: Optional[List[Planningposition]] = [] 
    taxablePortion: Optional[List[Planningposition]] = []
    incomeTaxPosition_id: int

    # Class-attribute
    instanceDic: ClassVar[dict] = {}

    #Init-Function and adding to instanceDic
    def __init__(self, **data):
        """
        not using self.__class__ sinc if the object gets created by another class which inherits from this one, 
        self.__class__ refers on the class the object gets actually created
        """
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, Income.instanceDic)
        Income.instanceDic[self.name] = self

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
