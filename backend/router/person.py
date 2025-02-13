""" Class for data about the planningperson """


from logger_setup import logger
from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from typing import ClassVar, Optional
from generalClasses.monthYear import *
from utils.nameManager import *


class Person(BaseModel):
    #Object-attribute
    name: str
    birth: Optional[MonthYear] = None

    #Class-attribute
    instanceDic: ClassVar[dict] = {}
    place: ClassVar[str] = None

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Person":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic
        return obj


#starting router
router = APIRouter(prefix="/person", tags=["person"])

#creating a new cedit-object
@router.post("/create-person/")
def create_person(name: str):
    try:
        new_object = Person.create(name=name)
        logger.debug({"New object created": new_object.name})
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()


# Returns person position by name
@router.get("/get-person/{name}")
def get_person(name: str):
    if name is None:
        return None
    elif name not in Person.instanceDic:
        return {"Error": "name not found"}
    return Person.instanceDic[name]

# Returns all Persons
@router.get("/get-allPersons/")
def get_allPersons():
    return Person.instanceDic
