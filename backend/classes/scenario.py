""" Class for different scenarios in the planning """

from pydantic import BaseModel
from typing import ClassVar, List, Optional
from .monthYear import *



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
        cls.instanceDic[obj.name] = obj

        return obj



