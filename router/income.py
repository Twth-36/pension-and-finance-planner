""" Class Income for planning all possible incomes"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses import *
from .planningposition import Planningposition

class IncomeEvents(BaseModel):
    scenario_id: int 
    eventDate: monthYear.MonthYear
    newValue: Optional[float]
    percentageAdjustment: Optional[float]
    inEventDoc: bool
    eventDecription: Optional[str]

class Income(Planningposition):
    changes: Optional[List[IncomeEvents]] = Field(default_factory=list)

#Dictionary for managing all income position
incomeDic = {}

#starting router
router = APIRouter()
