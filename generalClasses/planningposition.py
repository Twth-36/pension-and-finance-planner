"""Class for general planningposition"""

from pydantic import BaseModel
from generalClasses.monthYear import *
from typing import Optional
from router import *

class Planningposition(BaseModel):
    scenario_id: Scenario
    period: MonthYear
    value: float
    inDoc: bool
    description: Optional[str] = None






