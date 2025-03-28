"""
Class Income for planning all possible incomes

Objects can't get created via API! see manualIncome
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List
from classes.cashflow import Cashflow
from planningposition import *
from person import *
from incomeTaxPos import *
from scenario import *


class Income(BaseModel):
    # Object-attributes
    name: str
    person: Optional[Person] = None
    planValue: Optional[List[Planningposition]] = []
    taxablePortion: Optional[float] = 1
    taxPosition: Optional[IncomeTaxPos] = None

    # Class-attribute
    instanceDic: ClassVar[dict] = {}
    cashflowPos: ClassVar[Cashflow] = None  # cashlowposition on which the total flows

    # create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Income":
        # Create and validate and add to instanceDic
        obj = cls.model_validate(data)
        obj.name = generate_uniqueName(obj.name, cls.instanceDic)
        cls.instanceDic[obj.name] = obj

        # if incomeTaxPosition not exisiting, creating one
        if obj.taxPosition is None:
            obj.taxPosition = IncomeTaxPos.create(name=obj.name, person=obj.person)

        return obj
