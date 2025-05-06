from backend.classes.expense import Expense
from backend.classes.income import Income
from backend.classes.incomeTaxPos import IncomeTaxPos
from backend.classes.manualExpense import ManualExpense
from backend.classes.manualIncome import ManualIncome
from backend.classes.manualIncomeTaxPos import ManualIncomeTaxPos
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.tax.taxproperties import TaxPositionType
from backend.utils.monthYear import MonthYear


def exe_incomeTaxPosPlanning(period: MonthYear, scenario: Scenario):
    """prepares planningPosition in planValue for each object in instanceDic"""

    for obj in IncomeTaxPos.instanceDic.values():
        # check if planPos exist
        if (
            Planningposition.get_item(
                period=period, scenario=scenario, list=obj.planValue
            )
            is None
        ):
            # add new empty-object to planValue
            Planningposition(scenario=scenario, period=period).add_toList(obj.planValue)


def exe_manualIncomeTaxPosPlanning(period: MonthYear, scenario: Scenario):

    if period.month == 12:
        # work through every object in instanceDic:
        for obj in ManualIncomeTaxPos.instanceDic.values():

            # create new Planningposition
            new_pos = Planningposition(scenario=scenario, period=period)

            # find last fixed Value
            fix_pos = Planningposition.get_lastItem(
                startDate=Scenario.baseDate,
                endDate=period,
                scenario=scenario,
                list=obj.fixValue,
            )

            if fix_pos:
                new_pos.value = fix_pos.value
                if fix_pos.period == period:
                    new_pos.description = fix_pos.description
            else:  # if no fixValue in past, then baseValue
                new_pos.value = obj.baseValue

            if obj.type == TaxPositionType.deduction:
                new_pos.value = -new_pos.value  # if deduction change sign

            # add new position planValue
            new_pos.add_toList(obj.planValue)


def exe_completeIncomeTaxPosPlanning(period: MonthYear, scenario: Scenario):

    # work through all income, manualIncome, Expense, manualExpense objects
    classes = [ManualIncome, Income, ManualExpense, Expense]
    for cls in classes:
        for obj in cls.instanceDic.values():
            obj_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.planValue
            )
            obj_taxPos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.taxPosition.planValue
            )
            obj_taxPos.value += obj_pos.value * obj.taxablePortion / 100
