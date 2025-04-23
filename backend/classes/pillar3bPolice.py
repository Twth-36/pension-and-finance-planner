"""Class for organising pillar 3b polices"""

from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List

from backend.utils.payFrequency import PayFrequency
from .planningposition import *
from .expense import *
from .income import *


class Pillar3bPolice(BaseModel):
    # Object-Variables
    name: str
    person: Person
    baseValue: Optional[float] = 0
    planValue: Optional[List[Planningposition]] = []
    expPayoutValue: Optional[float] = 0
    expPensionValue: Optional[float] = 0
    deposit: Optional[float] = 0
    depositFreq: PayFrequency = PayFrequency.Y
    payoutDate: MonthYear

    depositExpense: Optional[Expense] = None
    payoutCF: Optional[Cashflow] = None
    pensionIncome: Optional[Income] = None

    # Class-variables
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

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} may not be negative")
        return baseValue

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Pillar3bPolice":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic

        if obj.depositExpense is None:
            param = {"name": "Einzahlung: " + obj.name, "taxablePortion": 0}
            if obj.person:
                param["person"] = obj.person
            obj.depositExpense = Expense.create(**param)

        if obj.payoutCF is None:
            param = {"name": "Auszahlung: " + obj.name, "taxablePortion": 0}
            if obj.person:
                param["person"] = obj.person
            obj.payoutCF = Cashflow.create(**param)

        if obj.pensionIncome is None:
            param = {"name": "Rente: " + obj.name, "taxablePortion": 0}
            if obj.person:
                param["person"] = obj.person
            obj.pensionIncome = Income.create(**param)

        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "Pillar3bPolice":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        del self.__class__.instanceDic[self.name]


# rebuild model to ensure other classes are loaded
Pillar3bPolice.model_rebuild()
