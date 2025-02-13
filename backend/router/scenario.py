""" Class for different scenarios in the planning """

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from typing import ClassVar, List, Optional
from generalClasses.monthYear import *
from router.person import Person, get_person
from utils.nameManager import generate_uniqueName


class Scenario(BaseModel):
    # Objectvariable
    name: str

    # classvariable
    baseDate: ClassVar[MonthYear] = get_lastYearLastMonth()
    endDate: ClassVar[MonthYear] = MonthYear(month=get_currentDate().month, year=get_currentDate().year + 10)
    
    instanceDic: ClassVar[dict] = {}


    #create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "Scenario":
        #Create and validate and add to instanceDic
        obj = cls.model_validate(data)
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) 
        cls.instanceDic[obj.name] = obj

        return obj


#starting router
router = APIRouter(prefix="/scenario", tags=["scenario"])

#creating a new cedit-object
@router.post("/create-scenario/")
def create_scenario(name: str):
    try:
        new_object = Scenario.create(name=name)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) #422 for "Unprocessable Entity response"
    return new_object.model_dump()



