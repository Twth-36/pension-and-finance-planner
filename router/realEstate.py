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