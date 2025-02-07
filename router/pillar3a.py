""" Class for organising pillar 3a """

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List
from generalClasses.nameManager import *
from generalClasses.planningposition import *
from enum import Enum
from router.expense import *

class Pillar3aType(Enum):
    account = 0
    depot = 1
    police = 2

class Pillar3a(BaseModel):
    # Object-Variables
    name: str
    person: Person
    type: Pillar3aType
    baseValue: float
    fixValue: Optional[List[Planningposition]] = [] #only for polices
    planValue: Optional[List[Planningposition]] = []
    endDate: Optional[MonthYear] = None #when it gets withdrawed or the police ends
    returnRate: Optional[List[Planningposition]] = []
    depositExpense: Optional[Expense] = None # expense Position where deposits are accounted

    #Class-variables
    pillar3aDic: ClassVar[dict] = {}

    # Init-Function and adding to instanceDic
    def __init__(self, **data):
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, self.__class__.instanceDic)
        self.__class__.instanceDic[self.name] = self

#starting router
router = APIRouter(prefix="/pillar3a", tags=["pillar3a"])

#creating a new pillar3a-object
@router.post("/create-pillar3a/")
def create_pillar3a(new_object: Pillar3a):
    return new_object.__class__.instanceDic[new_object.name]

# Deleting an existing pillar3a object
@router.delete("/delete-pillar3a/{object_name}")
def delete_pillar3a(object_name: str):
    if object_name not in Pillar3a.instanceDic:
        return {"Error": "object_name not found"}
    
    del Pillar3a.instanceDic[object_name]
    return {"Success": "Pillar3a deleted"}

# Returns pillar3a position by name
@router.get("/get-pillar3a/{object_name}")
def get_pillar3a(object_name: str):
    if object_name not in Pillar3a.instanceDic:
        return {"Error": "object_name not found"}
    return Pillar3a.instanceDic[object_name]

# Returns all Pillar3as
@router.get("/get-allPillar3as/")
def get_allpillar3as():
    return Pillar3a.instanceDic