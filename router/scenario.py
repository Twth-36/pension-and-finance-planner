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
    baseDate: ClassVar[MonthYear] = get_lastYearLastMonth
    endDate: ClassVar[MonthYear] = get_lastYearLastMonth




#starting router
router = APIRouter(prefix="/scenario", tags=["scenario"])



