""" Class Expense for planning all possible expenses"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses.planningposition import *


class Expense(BaseModel):
    name: str
    person_id: int
    currentValue: List[Planningposition]
    taxableRate: List[Planningposition]
    inflationRate: List[Planningposition] 

#Dictionary for managing all income position
expenseDic = {}

#starting router
router = APIRouter()
