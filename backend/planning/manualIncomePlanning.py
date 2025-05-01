from backend.classes.manualIncome import ManualIncome
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.utils.monthYear import MonthYear


def exe_manualIncomePlanning(period: MonthYear, scenario: Scenario):

    # work through every object in instanceDic:
    for obj in ManualIncome.instanceDic.values():

        # create new Planningposition
        new_pos = Planningposition(scenario=scenario, period=period)

        # find previous Planningposition
        prev_pos = Planningposition.get_item(
            period=period.nextMonth(-1), scenario=scenario, list=obj.planValue
        )

        # make initial PlanValue
        if prev_pos is None:  # case if first planningMonth
            new_pos.value = obj.baseValue
        else:
            new_pos.value = prev_pos.value

        # searched for fixValue
        fixValue_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.fixValue
        )

        # if fixValue available overwrite PlanPosition
        if fixValue_pos:
            new_pos.value = fixValue_pos.value
            new_pos.description = fixValue_pos.description

        # add new position planValue
        new_pos.add_toList(obj.planValue)
