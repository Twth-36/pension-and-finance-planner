"""realEstates inlcusive renovations etc."""

from typing import Optional, List
from .planningposition import *  # issue why necessary?
from pydantic import BaseModel, field_validator
from .monthYear import *
from .expense import *
from .person import *
from .scenario import *


class RealEstate(BaseModel):
    # Object-variable
    name: str
    person: Optional[Person] = None
    baseValue: Optional[float] = 0
    planValue: Optional[List[Planningposition]] = None

    baseTaxValue: Optional[float] = None
    taxValue: Optional[List[Planningposition]] = []
    taxRate: Optional[float] = None
    taxCF: Optional[Cashflow] = None

    maintCostRate: float = None
    maintenanceExpense: Optional[Expense] = None

    renovations: Optional[List[Planningposition]] = []
    renovationExpense: Optional[Expense] = None

    purchase: Optional[List[Planningposition]] = []
    purchaseCF: Optional[Cashflow] = None

    sale: Optional[List[Planningposition]] = []
    saleCF: Optional[Cashflow] = None

    # Class-variable
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
    def create(cls, **data) -> "RealEstate":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic
        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "RealEstate":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        del self.__class__.instanceDic[self.name]
