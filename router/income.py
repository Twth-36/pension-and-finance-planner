""" Class Income for planning all possible incomes"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses.planningposition import *


class Income(BaseModel):
    name: str
    person_id: int
    currentValue: List[Planningposition]
    taxableRate: List[Planningposition]

#Dictionary for managing all income position
incomeDic = {}

#starting router
router = APIRouter()
