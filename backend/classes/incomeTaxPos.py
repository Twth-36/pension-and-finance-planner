"""
Positions to calculate incomeTax
(not only for incomes, also for expense i.e. all relevant positions to calculate the incometax)

Objects can't get created via API! see manualIncomeTaxPos
"""

from pydantic import BaseModel
from typing import List, Optional, ClassVar

from .person import *
from .planningposition import *

"""
Class for all incometax positions, which depend directly on an income or expense-object
Examples: income by labor, interest-payments
"""


class IncomeTaxPos(BaseModel):
    # Object-attributes
    name: str
    person: Optional[Person] = None
    planValue: Optional[List[Planningposition]] = []
    type: Optional[TaxPositionType] = TaxPositionType.income

    # Class-attribute
    instanceDic: ClassVar[dict] = {}

    # Validation for unique name
    @field_validator("name", mode="after")
    @classmethod
    def check_uniquename(cls, name: str) -> str:
        if name == "":
            raise ValueError(f"May not be empty")
        if name in cls.instanceDic:
            raise ValueError(f"An object with name '{name}' already exists")
        return name

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "IncomeTaxPos":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic
        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "IncomeTaxPos":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        del self.__class__.instanceDic[self.name]


# rebuild model to ensure other classes are loaded
IncomeTaxPos.model_rebuild()
