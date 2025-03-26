""" Credit inclusive interest and backpayments"""

from typing import Optional, List, ClassVar
from generalClasses import *
from pydantic import BaseModel, field_validator
from utils.nameManager import *
from expense import *
from scenario import *
from person import *
from monthYear import *
from planningposition import *

class Credit(BaseModel):
    # Object-attributes
    name: str
    person: Optional[Person] = None
    endDate: Optional[MonthYear] = Scenario.endDate
    baseValue: Optional[float] = 0
    planValue: Optional[List[Planningposition]] = []

    interestRate: Optional[List[Planningposition]] = [] #p.a.
    interstExpense: Optional[Expense] = None
    
    payback: Optional[List[Planningposition]] = []
    paybackCF: Optional[Cashflow] = None

    increase: Optional[List[Planningposition]] = []
    increaseCF: Optional[Cashflow] = None

    realEstate: Optional[Expense] = None #if mortgage

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    @field_validator('baseValue', mode='after')  
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f'{baseValue} may not be negative')
        return baseValue 
    
    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Credit":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic
        return obj
