from typing import ClassVar, List, Optional
from pydantic import BaseModel, field_validator

from backend.classes.person import Person
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario


class Planningobject(BaseModel):
    # Object-attributes
    name: str
    person: Optional[Person] = None
    planValue: Optional[List[Planningposition]] = []

    # Class-attribute
    """gets overwritten in ever sub-class, since we want
    a Dic for every class on his own"""
    instanceDic: ClassVar[dict] = {}

    # Validation for unique name
    @field_validator("name", mode="after")
    @classmethod
    def check_uniquename(cls, name: str) -> str:
        if name == "":
            raise ValueError(f"May not be empty")
        if name in cls.instanceDic:
            raise ValueError(
                f"An {cls.__name__}-object with name '{name}' already exists"
            )
        return name

    @field_validator("person", mode="before")
    @classmethod
    def _load_person(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Person.get_itemByName(v["name"])
        return v

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Planningposition":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic

        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "Planningposition":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        del self.__class__.instanceDic[self.name]

    def reset_planValue(self, scenario: Scenario):
        # delets all planValue of an object with a specific scenario
        if not self.planValue:
            return
        self.planValue = [p for p in self.planValue if p.scenario != scenario]

    @classmethod
    def reset_allPlanValue(cls, scenario: Scenario):
        # delets all planValue of all objects with a specific scenario
        for obj in cls.instanceDic.values():
            obj.reset_planValue(scenario=scenario)

    @classmethod
    def copy_toNewScenario(cls, new_scenario: Scenario, src_scenario: Scenario):
        # empty function in case the function is not overwritten in subclass
        return
