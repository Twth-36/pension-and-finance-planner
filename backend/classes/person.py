"""Class for data about the planningperson"""

from backend.logger_setup import logger
from pydantic import BaseModel, ConfigDict, field_validator
from typing import ClassVar, Optional
from backend.tax.taxproperties import *
from .monthYear import *


class Person(BaseModel):
    # Object-attribute
    name: str
    birth: MonthYear
    conf: Confession

    # Class-attribute
    instanceDic: ClassVar[dict] = {}
    place: ClassVar[str] = None
    taxation: ClassVar[Taxation] = Taxation.single

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
    def create(cls, **data) -> "Person":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic
        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "Person":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        # check first if objects is still used anywhere
        ##TODO
        del self.__class__.instanceDic[self.name]
