"""Class for general planningposition"""

from pydantic import BaseModel
from generalClasses.monthYear import MonthYear
from typing import Optional


class Planningposition(BaseModel):
    scenario_id: Optional[int] = 0
    period: MonthYear
    value: Optional[float] = 0
    inDoc: Optional[bool] = False
    description: Optional[str] = None






