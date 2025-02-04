""" Class for data about the planningperson """
from fastapi import APIRouter, Path
from pydantic import BaseModel
from typing import Optional
from generalClasses import *


class Person(BaseModel):
    name: str
    birth: monthYear.MonthYear
    ZIPCode: int

#Dictionary for managing the planning persons
personDic = {
    1: {
        "name": "John",
        "birth": {"month": 8, "year": 1997},
        "ZIPCode": 2552
    },
    2: {
        "name": "Johnine",
        "birth": {"month": 8, "year": 1997},
        "ZIPCode": 2552
    },
    3: {"name": "gemeinsam",
        "birth": None,
        "ZIPCode:": 2552
        }
}

#Starting router
router = APIRouter()

@router.get("/person/get-person/{person_id}")
def get_person(person_id: int):
    if person_id not in personDic:
        return {"Error": "person_id not found"}
    return personDic[person_id]

@router.put("/person/update-person/{person_id}")
def update_person(person_id: int, person: Person):
    if person_id not in personDic:
        return {"Error": "person_id not found"}
    personDic[person_id].update(person)
    return personDic[person_id]

