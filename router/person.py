""" Class for data about the planningperson """
from fastapi import APIRouter, Path
from pydantic import BaseModel
from typing import ClassVar, Optional
from generalClasses.monthYear import *


class Person(BaseModel):
    #Object-attribute
    name: str
    birth: Optional[MonthYear] = None

    #Class-attribute
    personCounter: ClassVar[int] = 2 # Represents if the plan is for a single person or a couple
    personDic: ClassVar[dict] = {
        0: {
            "name": "Andy",
            "birth": {"month": 8, "year": 1975}
        },
        1: {
            "name": "Lou",
            "birth": {"month": 11, "year": 1977}
        },
        2: {"name": "gemeinsam",
            "birth": None
            }
    }




# Dictionary for managing the planning persons
# The person-objects are fixed and can only be changed, but not created since the Planner works only for a single person or (married by tax-reason) couple


# Starting router
router = APIRouter(prefix="/person", tags=["person"])

# Changes liquidity reserve
@router.put("/put-newPersonCounter/{personCounter}")
def put_newPersonCounter(personCounter: float):
    Person.personCounter = personCounter
    return Person.personCounter

# Returns person position by name
@router.get("/get-credit/{object_name}")
def get_credit(object_name: str):
    if object_name not in Person.instanceDic:
        return {"Error": "object_name not found"}
    return Person.instanceDic[object_name]

# Returns all Persons
@router.get("/get-allPersons/")
def get_allPersons():
    return Person.instanceDic
