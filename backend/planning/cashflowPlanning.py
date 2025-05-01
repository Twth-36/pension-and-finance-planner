from backend.classes.cashflow import Cashflow
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.utils.monthYear import MonthYear


def exe_cashflowPlanning(period: MonthYear, scenario: Scenario):
    """prepares planningPosition in planValue for each object in instanceDic"""

    for obj in Cashflow.instanceDic.values():
        # check if planPos exist
        if (
            Planningposition.get_item(
                period=period, scenario=scenario, list=obj.planValue
            )
            is None
        ):
            # add new empty-object to planValue
            Planningposition(scenario=scenario, period=period).add_toList(obj.planValue)
