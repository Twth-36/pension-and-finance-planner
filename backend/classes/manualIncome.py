"""Class ManualIncome for planning all possible incomes, which do not depend on another object (unlike pension etc.)"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from .planningposition import *
from .income import *
from .incomeTaxPos import *
from .person import *
from .cashflow import *


class ManualIncome(Income):
    # Object-attributes
    baseValue: Optional[float] = 0  # p.a.
    fixValue: Optional[List[Planningposition]] = []  # overturns planning value

    # Class-attribute
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
ManualIncome.model_rebuild()
