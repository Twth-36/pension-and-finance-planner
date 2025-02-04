""" Class for data about the planningperson """
from fastapi import APIRouter, Path
from pydantic import BaseModel
from typing import Optional


class Person(BaseModel):
    name: str
    birthmonth: int
    birthyear: int
    ZIPCode: int

personDic = {
    1: {
        "name": "John",
        "birthmonth": 8,
        "birthyear": 1998,
        "ZIPCode": 2552
    },
    2: {
        "name": "Johnine",
        "birthmonth": 7,
        "birthyear": 1995,
        "ZIPCode": 2552
    },
    3: {"surname": "gemeinsam",
        "prename": None,
        "birthmonth": None,
        "birthyear": None,
        "ZIPCode:": 2552
        }
}

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

