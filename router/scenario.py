""" Class for different scenarios in the planning """

from pydantic import BaseModel
from fastapi import APIRouter
from typing import ClassVar, List, Optional
from generalClasses.monthYear import *
from router.person import Person


class Scenario(BaseModel):
    # Objectvariable
    description: str

    # classvariable
    baseDate: ClassVar[MonthYear] = get_lastYearLastMonth()
    endDate: ClassVar[MonthYear] = MonthYear(month=get_currentDate().month, year=get_currentDate().year + 10)




#starting router
router = APIRouter(prefix="/scenario", tags=["scenario"])



