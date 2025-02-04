"""Class for general planningposition"""

from pydantic import BaseModel
from monthYear import *
from typing import Optional

class Planningposition(BaseModel):
    value: float
    period: MonthYear
    inDoc: bool
    description: Optional[str] = None






