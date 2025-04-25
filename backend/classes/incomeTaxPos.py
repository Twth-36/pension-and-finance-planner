"""
Positions to calculate incomeTax
(not only for incomes, also for expense i.e. all relevant positions to calculate the incometax)

Objects can't get created via API! see manualIncomeTaxPos
"""

from pydantic import BaseModel
from typing import List, Optional, ClassVar

from backend.classes.planningobject import Planningobject

from .person import *
from .planningposition import *

"""
Class for all incometax positions, which depend directly on an income or expense-object
Examples: income by labor, interest-payments
"""


class IncomeTaxPos(Planningobject):
    # Object-attributes
    type: Optional[TaxPositionType] = TaxPositionType.income

    # Class-attribute
    instanceDic: ClassVar[dict] = {}


# rebuild model to ensure other classes are loaded
IncomeTaxPos.model_rebuild()
