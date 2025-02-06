""" Class for Pensionfund inclusive organising withdrawal as capital or pension """

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses.planningposition import *

class PensionFund(BaseModel):
    name: str
    person_id: int
    baseValue: float
    fixValue: Optional[List[Planningposition]] = []
    planValue: Optional[List[Planningposition]] = []
    savingContribution: Optional[List[Planningposition]] = [] #dt: Sparbeitrag (monthly)
    returnRate: Optional[List[Planningposition]] = []
    withdrawalPortion: Optional[List[Planningposition]] = [] # Portion which gets withdrawed as part of a (partly-)Pension
    capitalPortion: Optional[List[Planningposition]] = [] # Portion OF THE WITHDRAWED pensioncapital which gets paid out as capital
    conversionRate: Optional[List[Planningposition]] = [] # dt: Umwandlungssatz

#Dictionary for managing all pensionFund positions
pensionFundDic = {}

#starting router
router = APIRouter(prefix="/pensionFund", tags=["pensionFund"])


#creating a new pensionFund-object
@router.post("/pensionFund/create-pensionFund/{pensionFund_id}")
def create_pensionFund(pensionFund_id: int, pensionFund: PensionFund):
    if pensionFund_id in pensionFundDic:
        return {"Error": "pensionFund_id already used"}
    
    pensionFundDic[pensionFund_id] = pensionFund
    return pensionFundDic[pensionFund_id]

# Changes on existing pensionFund-object
@router.put("/pensionFund/update-pensionFund/{pensionFund_id}")
def update_pensionFund(pensionFund_id: int, pensionFund: PensionFund):
    if pensionFund_id not in pensionFundDic:
        return {"Error": "pensionFund_id not found"}
    
    pensionFundDic[pensionFund_id].update(pensionFund)
    return pensionFundDic[pensionFund_id]

# Deleting an existing pensionFund object
@router.delete("/pensionFund/delete-pensionFund/{pensionFund_id}")
def delete_pensionFund(pensionFund_id: int):
    if pensionFund_id not in pensionFundDic:
        return {"Error": "pensionFund_id not found"}
    
    del pensionFundDic[pensionFund_id]
    return {"Success": "pensionFund deleted"}

# Returns pensionFund position by id
@router.get("/pensionFund/get-pensionFund/{pensionFund_id}")
def get_pensionFund(pensionFund_id: int):
    if pensionFund_id not in pensionFundDic:
        return {"Error": "pensionFund_id not found"}
    return pensionFundDic[pensionFund_id]

# Returns all pensionFunds
@router.get("/pensionFund/get-allpensionFunds/")
def get_allpensionFunds():
    return pensionFundDic