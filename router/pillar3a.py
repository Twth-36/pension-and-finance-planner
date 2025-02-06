""" Class for organising pillar 3a """

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from generalClasses.planningposition import *
from enum import Enum

class Pillar3aType(Enum):
    account = 0
    depot = 1
    police = 2

class Pillar3a(BaseModel):
    name: str
    person_id: int
    type: Pillar3aType
    baseValue: float
    fixValue: Optional[List[Planningposition]] = [] #only for polices
    planValue: Optional[List[Planningposition]] = []
    endDate: Optional[MonthYear] = None #when it gets withdrawed or the police ends
    returnRate: Optional[List[Planningposition]] = []
    expensePosition_id: Optional[int] = None # expense Position where deposits are accounted

 #Dictionary for managing all pillar3a position
pillar3aDic = {}

#starting router
router = APIRouter(prefix="/pillar3a", tags=["pillar3a"])

#creating a new pillar3a-object
@router.post("/create-pillar3a/{pillar3a_id}")
def create_pillar3a(pillar3a_id: int, pillar3a: Pillar3a):
    if pillar3a_id in pillar3aDic:
        return {"Error": "pillar3a_id already used"}
    
    pillar3aDic[pillar3a_id] = pillar3a
    return pillar3aDic[pillar3a_id]

# Changes on existing pillar3a-object
@router.put("/update-pillar3a/{pillar3a_id}")
def update_pillar3a(pillar3a_id: int, pillar3a: Pillar3a):
    if pillar3a_id not in pillar3aDic:
        return {"Error": "pillar3a_id not found"}
    
    pillar3aDic[pillar3a_id].update(pillar3a)
    return pillar3aDic[pillar3a_id]

# Deleting an existing pillar3a object
@router.delete("/delete-pillar3a/{pillar3a_id}")
def delete_pillar3a(pillar3a_id: int):
    if pillar3a_id not in pillar3aDic:
        return {"Error": "pillar3a_id not found"}
    
    del pillar3aDic[pillar3a_id]
    return {"Success": "pillar3a deleted"}

# Returns pillar3a position by id
@router.get("/get-pillar3a/{pillar3a_id}")
def get_pillar3a(pillar3a_id: int):
    if pillar3a_id not in pillar3aDic:
        return {"Error": "pillar3a_id not found"}
    return pillar3aDic[pillar3a_id]

# Returns all pillar3as
@router.get("/get-allpillar3as/")
def get_allpillar3as():
    return pillar3aDic


