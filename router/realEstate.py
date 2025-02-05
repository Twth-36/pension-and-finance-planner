""" realEstates inclusive mortgages, renovations and  """

from fastapi import APIRouter, Path
from typing import Optional, List
from generalClasses import *
from generalClasses.planningposition import * #issue why necessary?
from pydantic import BaseModel


class RealEstate(BaseModel):
    taxValue: List[Planningposition]
    realEstateTaxRate: List[Planningposition]
    maintenanceCostRate: float


class Credit(BaseModel):
    interestRate: List[Planningposition]
    endDate: MonthYear
    realEstate_id: Optional[int] = None #if mortgage


realEstateDic = {}

creditDic = {}

router = APIRouter()

### Functions for RealEstate-class

#creating a new realEstate-object
@router.post("/realEstate/create-realEstate/{realEstate_id}")
def create_realEstate(realEstate_id: int, realEstate: RealEstate):
    if realEstate_id in realEstateDic:
        return {"Error": "realEstate_id already used"}
    
    realEstateDic[realEstate_id] = realEstate
    return realEstateDic[realEstate_id]

# Changes on existing realEstate-object
@router.put("/realEstate/update-realEstate/{realEstate_id}")
def update_realEstate(realEstate_id: int, realEstate: RealEstate):
    if realEstate_id not in realEstateDic:
        return {"Error": "realEstate_id not found"}
    
    realEstateDic[realEstate_id].update(realEstate)
    return realEstateDic[realEstate_id]

# Deleting an existing realEstate object
@router.delete("/realEstate/delete-realEstate/{realEstate_id}")
def delete_realEstate(realEstate_id: int):
    if realEstate_id not in realEstateDic:
        return {"Error": "realEstate_id not found"}
    
    del realEstateDic[realEstate_id]
    return {"Success": "realEstate deleted"}

# Returns realEstate position by id
@router.get("/realEstate/get-realEstate/{realEstate_id}")
def get_realEstate(realEstate_id: int):
    if realEstate_id not in realEstateDic:
        return {"Error": "realEstate_id not found"}
    return realEstateDic[realEstate_id]

# Returns all realEstates
@router.get("/realEstate/get-allrealEstates/")
def get_allrealEstates():
    return realEstateDic


### Functions for Credit-class

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