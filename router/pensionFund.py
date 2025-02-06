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
incomeDic = {}

#starting router
router = APIRouter()


