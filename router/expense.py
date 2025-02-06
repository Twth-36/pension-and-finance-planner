""" Class Expense for planning all possible expenses"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses.planningposition import *


class Expense(BaseModel):
    name: str
    person_id: int
    baseValue: float #YEARLY
    fixValue: Optional[List[Planningposition]] = [] 
    planValue: Optional[List[Planningposition]] = []
    taxablePortion: Optional[List[Planningposition]] = []
    inflationRate: Optional[List[Planningposition]] = []

#Dictionary for managing all income position
expenseDic = {}

#starting router
router = APIRouter(prefix="/expense", tags=["expense"])


# Creating a new expense-object
@router.post("/create-expense/{expense_id}")
def creeate_expense(expense_id: int, expense: Expense):
    if expense_id in expenseDic:
        return {"Error": "expense_id already used"}
    
    expenseDic[expense] = expense
    return expenseDic[expense]

# Changes on existing expense-object
@router.put("/update-expense/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    if expense_id not in expenseDic:
        return {"Error": "expense_id not found"}
    
    expenseDic[expense_id].update(expense)
    return expenseDic[expense_id]

# Deleting an existing expense object
@router.delete("/delete-expense/{expense_id}")
def delete_expense(expense_id: int):
    if expense_id not in expenseDic:
        return {"Error": "expense_id not found"}
    
    del expenseDic[expense_id]
    return {"Success": "Expense deleted"}

# Returns expense position by id
@router.get("/get-expense/{expense_id}")
def get_expense(expense_id: int):
    if expense_id not in expenseDic:
        return {"Error": "expense_id not found"}
    return expenseDic[expense_id]

# Returns all Expenses
@router.get("/get-allexpenses/")
def get_allexpenses():
    return expenseDic

