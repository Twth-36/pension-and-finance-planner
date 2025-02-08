"""
Class for calculate incometax, which aren't connected to a income or expense-object (i.e. outcome is not seperatly listed as an expense-object)
Examples: single-household-deduction (Alleinstehendenabzug), professional expenses, donations
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, ClassVar
from generalClasses.planningposition import *
from utils.nameManager import *
from router.incomeTaxPos import *

class ManualIncomeTaxPos(IncomeTaxPos):
    # Object-attributes
    baseValue: float #YEARLY
    fixValue: Optional[List[Planningposition]] = [] #overturns planning value
    planValue: Optional[List[Planningposition]] = []

    # Class-attributes
    instanceDic: ClassVar[dict] = {} 

    # Init-Function and adding to instanceDic
    def __init__(self, **data):
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, self.__class__.instanceDic)
        self.__class__.instanceDic[self.name] = self

#starting router
router = APIRouter(prefix="/manualIncomeTaxPos", tags=["manualIncomeTaxPos"])

#creating a new manualIncomeTaxPos-object
@router.post("/create-manualIncomeTaxPos/")
def create_manualIncomeTaxPos(new_object: ManualIncomeTaxPos):
    return new_object.__class__.instanceDic[new_object.name]

# Deleting an existing manualIncomeTaxPos object
@router.delete("/delete-manualIncomeTaxPos/{object_name}")
def delete_manualIncomeTaxPos(object_name: str):
    if object_name not in ManualIncomeTaxPos.instanceDic:
        return {"Error": "object_name not found"}
    
    del ManualIncomeTaxPos.instanceDic[object_name]
    return {"Success": "manualIncomeTaxPos deleted"}

# Returns manualIncomeTaxPos position by name
@router.get("/get-manualIncomeTaxPos/{object_name}")
def get_manualIncomeTaxPos(object_name: str):
    if object_name not in ManualIncomeTaxPos.instanceDic:
        return {"Error": "object_name not found"}
    return ManualIncomeTaxPos.instanceDic[object_name]

# Returns all manualIncomeTaxPos
@router.get("/get-allManualIncomeTaxPos/")
def get_allmanualIncomeTaxPos():
    return ManualIncomeTaxPos.instanceDic




