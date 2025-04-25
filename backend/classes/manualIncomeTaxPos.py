"""
Class for calculate incometax, which aren't connected to a income or expense-object (i.e. outcome is not seperatly listed as an expense-object)
Examples: single-household-deduction (Alleinstehendenabzug), professional expenses, donations
"""

from pydantic import BaseModel, field_validator
from typing import List, Optional, ClassVar
from .planningposition import *
from .incomeTaxPos import *
from .person import *


class ManualIncomeTaxPos(IncomeTaxPos):
    # Object-attributes
    baseValue: float  # YEARLY
    fixValue: Optional[List[Planningposition]] = []  # overturns planning value

    # Class-attributes
    instanceDic: ClassVar[dict] = {}


# rebuild model to ensure other classes are loaded
ManualIncomeTaxPos.model_rebuild()
