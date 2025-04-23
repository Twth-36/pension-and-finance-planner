"""
Class for cashflows i.e. not relevant for income tax for example credit back payments etc.
"""

# for future importing Income due to circular import
from __future__ import annotations

from backend.classes.person import Person

from .planningposition import Planningposition
from typing import TYPE_CHECKING, ClassVar, Optional, List
from pydantic import BaseModel
from ..utils.monthYear import *
from .scenario import *

# import Income only for typechecking due to circular import
if TYPE_CHECKING:
    from classes.income import Income


## class for aggregated free assets i.e. liqudity and assets to generate income
class Cashflow(BaseModel):
    name: str
    person: Optional[Person] = None
    planValue: Optional[List[Planningposition]] = []
    taxablePortion: Optional[float] = (
        0  # for capital withdrawal tax (Kapitalauszahlungssteuer)
    )

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

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Cashflow":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic
        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "Cashflow":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        del self.__class__.instanceDic[self.name]


# rebuild model to ensure other classes are loaded
Cashflow.model_rebuild()
