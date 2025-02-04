""" Class Expense for planning all possible expenses"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses import *
from .planningposition import Planningposition

class ExpenseEvents(BaseModel):
    scenario_id: int 
    eventDate: monthYear.MonthYear
    newValue: Optional[float]
    percentageAdjustment: Optional[float]
    inEventDoc: bool
    eventDecription: Optional[str]

class Income(Planningposition):
    inflation: float
    changes: Optional[List[ExpenseEvents]] = Field(default_factory=list)

#Dictionary for managing all income position
expenseDic = {}

#starting router
router = APIRouter()
