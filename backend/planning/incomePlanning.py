from backend.classes.income import Income
from backend.classes.manualIncome import ManualIncome
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.utils.monthYear import MonthYear


def exe_incomePlanning(period: MonthYear, scenario: Scenario):
    """prepares planningPosition in planValue for each object in instanceDic"""

    for obj in Income.instanceDic.values():
        # check if planPos exist
        if (
            Planningposition.get_item(
                period=period, scenario=scenario, list=obj.planValue
            )
            is None
        ):
            # add new empty-object to planValue
            Planningposition(scenario=scenario, period=period).add_toList(obj.planValue)


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


def exe_completeIncomePlanning(period: MonthYear, scenario: Scenario):
    """total on cashflowposition"""
    income_sum = 0
    for obj in list(Income.instanceDic.values()) + list(
        ManualIncome.instanceDic.values()
    ):

        income_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.planValue
        )
        income_sum += income_pos.value

    # get cashflow pos for adding total
    expenseCF_pos = Planningposition.get_item(
        period=period, scenario=scenario, list=Income.cashflowPos.planValue
    )
    expenseCF_pos.value += income_sum
