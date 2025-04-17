"""Credit inclusive interest and backpayments"""

from typing import Optional, List, ClassVar
from pydantic import BaseModel, field_validator

from backend.classes.realEstate import *
from .expense import *
from .scenario import *
from .person import *
from .monthYear import *
from .planningposition import *


class Credit(BaseModel):
    # Object-attributes
    name: str
    person: Optional[Person] = None
    endDate: Optional[MonthYear] = None
    baseValue: Optional[float] = 0
    baseInterestRate: Optional[float] = 0
    planValue: Optional[List[Planningposition]] = []

    interestRate: Optional[List[Planningposition]] = []  # p.a.
    interestExpense: Optional[Expense] = None

    payback: Optional[List[Planningposition]] = []
    paybackCF: Optional[Cashflow] = None

    increase: Optional[List[Planningposition]] = []
    increaseCF: Optional[Cashflow] = None

    realEstate: Optional[RealEstate] = None  # if mortgage

    # Class-attributes
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
    def create(cls, **data) -> "Credit":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic

        if obj.interestExpense is None:
            param = {"name": "Zinszahlung: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.interestExpense = Expense.create(**param)

        if obj.increaseCF is None:
            param = {"name": "Krediterhöhung: " + obj.name}
            if obj.person:
                param["person"] = obj.person
            obj.increaseCF = Cashflow.create(**param)

        if obj.paybackCF is None:
            param = {"name": "Amortisation: " + obj.name}
            if obj.person:
                param["person"] = obj.person
            obj.paybackCF = Cashflow.create(**param)

        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "Credit":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        del self.__class__.instanceDic[self.name]


# rebuild model to ensure other classes are loaded
Credit.model_rebuild()
