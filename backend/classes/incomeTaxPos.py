"""
Positions to calculate incomeTax
(not only for incomes, also for expense i.e. all relevant positions to calculate the incometax)


"""

from typing import List, Optional, ClassVar

from backend.classes.planningobject import Planningobject

from .person import *
from .planningposition import *


class IncomeTaxPos(Planningobject):

    # Class-attribute
    instanceDic: ClassVar[dict] = {}


# rebuild model to ensure other classes are loaded
IncomeTaxPos.model_rebuild()
