"""Class ManualExpense for planning all possible expenses, which do not depend on another object (unlike mortgagepayments, taxes etc.)"""

from pydantic import BaseModel, Field
from typing import Optional, List
from .planningposition import *
from .expense import *
from .incomeTaxPos import *
from .person import *
from .cashflow import *


class ManualExpense(Expense):
    # Object-attributes
    baseValue: Optional[float] = 0  # per month
    fixValue: Optional[List[Planningposition]] = []  # overturns planning value
    inflationRate: float = 0
    repetitive: Optional[bool] = True

    # Class-attribute
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"baseValue: {baseValue} may not be negative")
        return baseValue


# rebuild model to ensure other classes are loaded
ManualExpense.model_rebuild()
