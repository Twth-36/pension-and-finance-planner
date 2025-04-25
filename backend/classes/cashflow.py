"""
Class for cashflows i.e. not relevant for income tax for example credit back payments etc.
"""

# for future importing Income due to circular import
from __future__ import annotations

from backend.classes.person import Person
from backend.classes.planningobject import Planningobject

from .planningposition import Planningposition
from typing import TYPE_CHECKING, ClassVar, Optional, List
from pydantic import BaseModel
from ..utils.monthYear import *
from .scenario import *

# import Income only for typechecking due to circular import
if TYPE_CHECKING:
    from classes.income import Income


## class for aggregated free assets i.e. liqudity and assets to generate income
class Cashflow(Planningobject):

    taxablePortion: Optional[float] = (
        0  # for capital withdrawal tax (Kapitalauszahlungssteuer)
    )

    # Class-attribute
    instanceDic: ClassVar[dict] = {}


# rebuild model to ensure other classes are loaded
Cashflow.model_rebuild()
