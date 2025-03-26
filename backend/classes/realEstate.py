""" realEstates inlcusive renovations etc. """

from typing import Optional, List
from generalClasses import *
from utils.nameManager import *
from planningposition import * #issue why necessary?
from pydantic import BaseModel, field_validator
from monthYear import *
from expense import *
from person import *
from scenario import *


class RealEstate(BaseModel):
    # Object-variable
    name: str
    person: Optional[Person] = None
    baseValue: Optional[float] = 0
    fixValue: Optional[List[Planningposition]] = None
    planValue: Optional[List[Planningposition]] = None

    ZIPCode: Optional[int] = None
    taxValue: Optional[List[Planningposition]] = None
    taxRate: Optional[List[Planningposition]] = None #only for dt: "Liegenschaftssteuer"

    maintCostRate: Optional[List[Planningposition]] = None
    maintenanceExpense: Optional[Expense] = None
    
    renovations: Optional[List[Planningposition]] = None
    renovationExpense: Optional[Expense] = None

    purchase: Optional[List[Planningposition]] = None
    purchaseCF: Optional[Cashflow] = None

    sale: Optional[List[Planningposition]] = None
    saleCF: Optional[Cashflow] = None

    # Class-variable
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator('baseValue', mode='after')  
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f'{baseValue} is strict smaller than 0')
        return baseValue
    
    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "RealEstate":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic
        return obj

