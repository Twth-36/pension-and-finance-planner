""" Class for data about the planningperson """
from fastapi import APIRouter, Path
from pydantic import BaseModel
from typing import Optional
from generalClasses import *


class Person(BaseModel):
    name: str
    birth: Optional[monthYear.MonthYear] = None


# Represents if the plan is for a single person or a (married) couple
personCounter = 2

# Dictionary for managing the planning persons
# The person-objects are fixed and can only be changed, but not created since the Planner works only for a single person or (married by tax-reason) couple
personDic = {
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

# Starting router
router = APIRouter(prefix="/person", tags=["person"])

# Returs person object by id
@router.get("/person/get-person/{person_id}")
def get_person(person_id: int):
    if person_id not in personDic:
        return {"Error": "person_id not found"}
    return personDic[person_id]

# Changes existing Person-object
@router.put("/person/update-person/{person_id}")
def update_person(person_id: int, person: Person):
    if person_id not in personDic:
        return {"Error": "person_id not found"}
    personDic[person_id].update(person)
    return personDic[person_id]

# Changes the number of persons (personCounter)
@router.put("/person/update-personCounter/{new_counterValue}")
def update_personCounter(new_CounterValue: int):
    personCounter = new_CounterValue

# Returns the current number of persons (personCounter)
@router.get("/person/get-personCounter/")
def get_PersonCounter():
    return personCounter
