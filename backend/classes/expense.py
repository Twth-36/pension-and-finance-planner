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

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Expense":
        obj = cls.model_validate(data)  # Creation and validation
        obj.name = generate_uniqueName(
            obj.name, cls.instanceDic
        )  # generate unique name
        cls.instanceDic[obj.name] = obj  # adding to instanceDic

        # if incomeTaxPosition not exisiting, creating one
        if obj.taxPosition is None:
            obj.taxPosition = IncomeTaxPos.create(name=obj.name, person=obj.person)

        return obj
