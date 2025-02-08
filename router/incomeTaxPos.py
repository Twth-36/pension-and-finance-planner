"""
Positions to calculate incomeTax
(not only for incomes, also for expense i.e. all relevant positions to calculate the incometax)

Objects can't get created via API! see manualIncomeTaxPos
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, ClassVar
from generalClasses.planningposition import *
from utils.nameManager import *

"""
Class for all incometax positions, which depend directly on an income or expense-object
Examples: income by labor, interest-payments
"""
class IncomeTaxPos(BaseModel):
    # Object-attributes
    name: str
    planValue: Optional[List[Planningposition]] = []

    # Class-attribute
    instanceDic: ClassVar[dict] = {}

    #Init-Function and adding to instanceDic
    def __init__(self, **data):
        """
        not using self.__class__ sinc if the object gets created by another class which inherits from this one, 
        self.__class__ refers on the class the object gets actually created
        """
        super().__init__(**data)
        self.name = generate_uniqueName(self.name, IncomeTaxPos.instanceDic)
        IncomeTaxPos.instanceDic[self.name] = self


#starting router
router = APIRouter(prefix="/incomeTaxPos", tags=["incomeTaxPos"])


# Returns all IncomeTaxPoss
@router.get("/get-incomeTaxPoss/")
def get_incomeTaxPoss():
    return IncomeTaxPos.instanceDic






