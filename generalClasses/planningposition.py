"""Class for general planningposition"""

from pydantic import BaseModel
from generalClasses.monthYear import MonthYear
from typing import Optional
from router.scenario import *


class Planningposition(BaseModel):
    scenario: Scenario
    period: MonthYear
    value: Optional[float] = 0
    inDoc: Optional[bool] = False
    description: Optional[str] = None






