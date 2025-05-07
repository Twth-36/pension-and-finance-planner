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

    # Object-attributes
    type: Optional[TaxPositionType] = TaxPositionType.income

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    @classmethod
    def copy_toNewScenario(cls, new_scenario: Scenario, src_scenario: Scenario):

        for obj in cls.instanceDic.values():
            # all lists with planValue where the scenario needs to be dublicated
            lists = [obj.planValue, obj.fixValue]

            # duplicates all scenario related fields to a newscenario
            for planPosList in lists:
                for pos in planPosList:
                    if pos.scenario == src_scenario:
                        Planningposition(
                            scenario=new_scenario,
                            period=pos.period,
                            value=pos.value,
                            inDoc=pos.inDoc,
                            description=pos.description,
                        ).add_toList(planPosList)


# rebuild model to ensure other classes are loaded
ManualIncomeTaxPos.model_rebuild()
