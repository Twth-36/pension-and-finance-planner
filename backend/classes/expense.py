"""
Class Expense for planning all possible expenses

Objects can't get created via API! see manualExpense
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from .cashflow import *
from .planningposition import *
from .incomeTaxPos import *
from .person import *


class Expense(BaseModel):
    # Object-attributes
    name: str
    person: Optional[Person] = None
    planValue: Optional[List[Planningposition]] = []
    taxablePortion: Optional[float] = 0
    taxPosition: Optional[IncomeTaxPos] = None

    # Class-attribute
    instanceDic: ClassVar[dict] = {}
    cashflowPos: ClassVar[Cashflow]

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
    def create(cls, **data) -> "Expense":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic

        if obj.taxPosition is None:
            param = {"name": obj.name, "type": TaxPositionType.deduction}
            if obj.person:
                param["person"] = obj.person
            obj.taxPosition = IncomeTaxPos.create(**param)

        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "Expense":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        del self.__class__.instanceDic[self.name]


# rebuild model to ensure other classes are loaded
Expense.model_rebuild()
