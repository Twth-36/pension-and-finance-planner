"""Class ManualIncome for planning all possible incomes, which do not depend on another object (unlike pension etc.)"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from .planningposition import *
from .income import *
from .incomeTaxPos import *
from .person import *
from .cashflow import *


class ManualIncome(Income):
    # Object-attributes
    baseValue: Optional[float] = 0  # p.a.
    fixValue: Optional[List[Planningposition]] = []  # overturns planning value

    # Class-attribute
    instanceDic: ClassVar[dict] = {}


# rebuild model to ensure other classes are loaded
ManualIncome.model_rebuild()
