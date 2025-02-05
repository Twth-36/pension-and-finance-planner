""" Credit inclusive interest and backpayments"""

from fastapi import APIRouter, Path
from typing import Optional, List
from generalClasses import *
from generalClasses.planningposition import * #issue why necessary?
from pydantic import BaseModel

class Credit(BaseModel):
    value: List[Planningposition]
    interestRate: List[Planningposition]
    endDate: MonthYear
    interstExpense_id: int
    realEstate_id: Optional[int] = None #if mortgage

creditDic = {}

#starting router
router = APIRouter()

#creating a new credit-object
@router.post("/credit/create-credit/{credit_id}")
def create_credit(credit_id: int, credit: Credit):
    if credit_id in creditDic:
        return {"Error": "credit_id already used"}
    
    creditDic[credit_id] = credit
    return creditDic[credit_id]

# Changes on existing credit-object
@router.put("/credit/update-credit/{credit_id}")
def update_credit(credit_id: int, credit: Credit):
    if credit_id not in creditDic:
        return {"Error": "credit_id not found"}
    
    creditDic[credit_id].update(credit)
    return creditDic[credit_id]

# Deleting an existing credit object
@router.delete("/credit/delete-credit/{credit_id}")
def delete_credit(credit_id: int):
    if credit_id not in creditDic:
        return {"Error": "credit_id not found"}
    
    del creditDic[credit_id]
    return {"Success": "Credit deleted"}

# Returns credit position by id
@router.get("/credit/get-credit/{credit_id}")
def get_credit(credit_id: int):
    if credit_id not in creditDic:
        return {"Error": "credit_id not found"}
    return creditDic[credit_id]

# Returns all Credits
@router.get("/credit/get-allcredits/")
def get_allcredits():
    return creditDic