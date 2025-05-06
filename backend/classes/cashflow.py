"""
Class for cashflows i.e. not relevant for income tax for example credit back payments etc.
"""

from backend.classes.planningobject import Planningobject


from typing import ClassVar, Optional
from ..utils.monthYear import *
from .scenario import *


## class for aggregated free assets i.e. liqudity and assets to generate income
class Cashflow(Planningobject):

    taxablePortion: Optional[float] = (
        0  # for capital withdrawal tax (Kapitalauszahlungssteuer)
    )

    # Class-attribute
    instanceDic: ClassVar[dict] = {}


# rebuild model to ensure other classes are loaded
Cashflow.model_rebuild()
