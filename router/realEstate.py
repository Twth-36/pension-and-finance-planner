""" realEstates inclusive mortgages, renovations and  """

from fastapi import APIRouter, Path
from typing import Optional, List
from generalClasses import *
from generalClasses.planningposition import *
from pydantic import BaseModel


class RealEstate(BaseModel):
    taxValue: List[Planningposition]
    realEstateTaxRate: List[Planningposition]
    maintenanceCostRate: float


class credit(BaseModel):
    interestRate: List[Planningposition]
    endDate: monthYear
    realEstate_id: Optional[int] = None #if mortgage


realEstateDic = {}

creditDic = {}

router = APIRouter()

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