"""Class for organising pillar 3a"""

from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List
from planningposition import *
from expense import *


class Pillar3a(BaseModel):
    # Object-Variables
    name: str
    person: Person
    baseValue: Optional[float] = 0
    planValue: Optional[List[Planningposition]] = []
    returnRate: Optional[List[Planningposition]] = []
    depositExpense: Optional[Expense] = (
        None  # expense Position where deposits are accounted
    )
    payoutCFpos: Optional[Cashflow] = None

    # Class-variables
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} is strict smaller than 0")
        return baseValue

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Pillar3a":
        obj = cls.model_validate(data)  # Creation and validation
        obj.name = generate_uniqueName(
            obj.name, cls.instanceDic
        )  # generate unique name
        cls.instanceDic[obj.name] = obj  # adding to instanceDic

        return obj


# Special class for Pillar3a Insurances
class Pillar3aInsurance(Pillar3a):
    fixDeposit: Optional[float] = 0  # p.a.
    endDate: Optional[MonthYear] = None
    endValue: Optional[float] = None  # fixed "Erlebensfallkapital"
    fixValue: Optional[List[Planningposition]] = []  # overturns planning value

    # Class-variables
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} is strict smaller than 0")
        return baseValue
