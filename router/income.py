""" Class Income for planning all possible incomes"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses.planningposition import *

class Income(BaseModel):
    name: str
    person_id: int
    baseValue: float #YEARLY
    fixValue: Optional[List[Planningposition]] = []
    planValue: Optional[List[Planningposition]] = []
    AHVrelevantIncome: Optional[bool] = False #relevant for calculation 'Säule 3a' payments
    taxablePortion: Optional[List[Planningposition]] = []

#Dictionary for managing all income position
incomeDic = {}

#starting router
router = APIRouter()

#creating a new income-object
@router.post("/income/create-income/{income_id}")
def create_income(income_id: int, income: Income):
    if income_id in incomeDic:
        return {"Error": "income_id already used"}
    
    incomeDic[income_id] = income
    return incomeDic[income_id]

# Changes on existing income-object
@router.put("/income/update-income/{income_id}")
def update_income(income_id: int, income: Income):
    if income_id not in incomeDic:
        return {"Error": "income_id not found"}
    
    incomeDic[income_id].update(income)
    return incomeDic[income_id]

# Deleting an existing income object
@router.delete("/income/delete-income/{income_id}")
def delete_income(income_id: int):
    if income_id not in incomeDic:
        return {"Error": "income_id not found"}
    
    del incomeDic[income_id]
    return {"Success": "Income deleted"}

# Returns income position by id
@router.get("/income/get-income/{income_id}")
def get_income(income_id: int):
    if income_id not in incomeDic:
        return {"Error": "income_id not found"}
    return incomeDic[income_id]

# Returns all Incomes
@router.get("/income/get-allincomes/")
def get_allincomes():
    return incomeDic