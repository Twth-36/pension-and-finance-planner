"""
Positions to calculate incomeTax
(not only for incomes, also for expense i.e. all relevant positions to calculate the incometax)

Objects can't get created via API! see manualIncomeTaxPos
"""

from pydantic import BaseModel
from typing import List, Optional, ClassVar
from planningposition import *
from utils.nameManager import *

"""
Class for all incometax positions, which depend directly on an income or expense-object
Examples: income by labor, interest-payments
"""
class IncomeTaxPos(BaseModel):
    # Object-attributes
    name: str
    person: Optional[Person] = None
    planValue: Optional[List[Planningposition]] = []

    # Class-attribute
    instanceDic: ClassVar[dict] = {}

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "IncomeTaxPos":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic
        return obj




