""" Top planning position for incomes, expenses assets and credits """

from pydantic import BaseModel
from typing import Optional

class Planningposition(BaseModel):
    name: str
    person_id: int
    initialValue: Optional[float] = 0





