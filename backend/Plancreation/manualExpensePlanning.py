from backend.classes.manualExpense import ManualExpense
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.utils.monthYear import MonthYear


def exe_manualExpensePlanning(period: MonthYear, scenario: Scenario):

    # work through every object in instanceDic:
    for obj in ManualExpense.instanceDic.values():

        # create new Planningposition
        new_pos = Planningposition(scenario=scenario, period=period)

        # find previous Planningposition
        prev_pos = Planningposition.get_item(
            period=period.nextMonth(-1), scenario=scenario, list=obj.planValue
        )

        if obj.repetitive == False:
            new_pos.value = 0
        elif prev_pos is None:  # case if first planningMonth
            new_pos.value = obj.baseValue
            new_pos.description = "Übernahme Basiswert"
        else:
            new_pos.value = prev_pos.value
            new_pos.description = "Fortführung Vormonatswert"

        # searched for fixValue
        fixValue = Planningposition.get_item(
            period=period, scenario=Scenario, list=obj.fixValue
        )

        # if fixValue available overwrite PlanPosition
        if fixValue:
            new_pos.value = fixValue.value
            new_pos.inDoc = fixValue.inDoc
            new_pos.description = fixValue.description
