""" Class ManualIncome for planning all possible incomes, which do not depend on another object (unlike pension etc.)"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from planningposition import *
from income import *
from incomeTaxPos import *
from person import *
from cashflow import *


class ManualIncome(Income):
    # Object-attributes
    baseValue: Optional[float] = 0 #p.a.
    fixValue: Optional[List[Planningposition]] = [] #overturns planning value

    # Class-attribute
    instanceDic: ClassVar[dict] = {}
    cashflowPos: ClassVar[Cashflow] #cashlowposition on which the total flows


    # Validation non-negative baseValue
    @field_validator('baseValue', mode='after')  
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f'{baseValue} is strict smaller than 0')
        return baseValue
    
