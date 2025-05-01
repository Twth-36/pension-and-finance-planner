from backend.classes.expense import Expense
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.utils.monthYear import MonthYear


def exe_expensePlanning(period: MonthYear, scenario: Scenario):
    """prepares planningPosition in planValue for each object in instanceDic"""

    for obj in Expense.instanceDic.values():
        # check if planPos exist
        if (
            Planningposition.get_item(
                period=period, scenario=scenario, list=obj.planValue
            )
            is None
        ):
            # add new empty-object to planValue
            Planningposition(scenario=scenario, period=period).add_toList(obj.planValue)
