"""Class for different scenarios in the planning"""

from pydantic import BaseModel, field_validator
from typing import ClassVar, List, Optional
from ..utils.monthYear import *


class Scenario(BaseModel):
    # Objectvariable
    name: str
    description: Optional[str] = None

    # classvariable
    baseDate: ClassVar[MonthYear] = MonthYear.get_lastYearLastMonth()
    endDate: ClassVar[MonthYear] = MonthYear(
        month=MonthYear.get_currentDate().month,
        year=MonthYear.get_currentDate().year + 10,
    )
    instanceDic: ClassVar[dict] = {}

    # Validation for unique name
    @field_validator("name", mode="after")
    @classmethod
    def check_uniquename(cls, name: str) -> str:
        if name == "":
            raise ValueError(f"May not be empty")
        if name in cls.instanceDic:
            raise ValueError(f"An object of with name '{name}' already exists")
        return name

    # create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Scenario":
        # Create and validate and add to instanceDic
        obj = cls.model_validate(data)
        cls.instanceDic[obj.name] = obj

        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "Scenario":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        # check first if objects is still used anywhere
        ##TODO
        del self.__class__.instanceDic[self.name]
