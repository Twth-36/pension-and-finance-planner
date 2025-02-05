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


# Creating a new expense-object
@router.post("/expense/create-expense/{expense_id}")
def creeate_expense(expense_id: int, expense: Expense):
    if expense_id in expenseDic:
        return {"Error": "expense_id already used"}
    
    expenseDic[expense] = expense
    return expenseDic[expense]

# Changes on existing expense-object
@router.put("/expense/update-expense/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    if expense_id not in expenseDic:
        return {"Error": "expense_id not found"}
    
    expenseDic[expense_id].update(expense)
    return expenseDic[expense_id]

# Deleting an existing expense object
@router.delete("/expense/delete-expense/{expense_id}")
def delete_expense(expense_id: int):
    if expense_id not in expenseDic:
        return {"Error": "expense_id not found"}
    
    del expenseDic[expense_id]
    return {"Success": "Expense deleted"}

# Returns expense position by id
@router.get("/expense/get-expense/{expense_id}")
def get_expense(expense_id: int):
    if expense_id not in expenseDic:
        return {"Error": "expense_id not found"}
    return expenseDic[expense_id]

# Returns all Expenses
@router.get("/expense/get-allexpenses/")
def get_allexpenses():
    return expenseDic

