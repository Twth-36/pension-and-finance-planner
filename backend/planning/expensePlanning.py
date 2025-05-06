from backend.classes.expense import Expense
from backend.classes.manualExpense import ManualExpense
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
            new_pos.value = -obj.baseValue
        else:
            new_pos.value = prev_pos.value

        # searched for fixValue
        fixValue_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.fixValue
        )

        # if fixValue available overwrite PlanPosition
        if fixValue_pos:
            new_pos.value = -fixValue_pos.value
            new_pos.description = fixValue_pos.description

        # add new position planValue
        new_pos.add_toList(obj.planValue)


def exe_completeExpensePlanning(period: MonthYear, scenario: Scenario):
    """total cashflowposition"""
    expense_sum = 0
    for obj in list(Expense.instanceDic.values()) + list(
        ManualExpense.instanceDic.values()
    ):

        expense_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.planValue
        )
        expense_sum += expense_pos.value

    # get cashflow pos for adding total
    expenseCF_pos = Planningposition.get_item(
        period=period, scenario=scenario, list=Expense.cashflowPos.planValue
    )
    expenseCF_pos.value += expense_sum
