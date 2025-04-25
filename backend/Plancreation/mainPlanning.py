from typing import List
from backend.Plancreation.manualExpensePlanning import exe_manualExpensePlanning
from backend.Plancreation.manualIncomePlanning import exe_manualIncomePlanning
from backend.classes.cashflow import Cashflow
from backend.classes.credit import Credit
from backend.classes.expense import Expense
from backend.classes.income import Income
from backend.classes.incomeTaxPos import IncomeTaxPos
from backend.classes.manualExpense import ManualExpense
from backend.classes.manualIncome import ManualIncome
from backend.classes.manualIncomeTaxPos import ManualIncomeTaxPos
from backend.classes.pensionFund import PensionFund
from backend.classes.pillar3a import Pillar3a
from backend.classes.pillar3aPolice import Pillar3aPolice
from backend.classes.pillar3bPolice import Pillar3bPolice
from backend.classes.realEstate import RealEstate
from backend.classes.scenario import Scenario
from backend.classes.vestedBenefit import VestedBenefit
from backend.utils.monthYear import MonthYear


def exe_mainPlanning(scenarios: List[Scenario]):

    # 0. Step make the plan for each scenario
    for scenario in scenarios:

        # 1. Step delete all old planValues
        classesToReset = [
            Cashflow,
            Credit,
            Expense,
            Income,
            IncomeTaxPos,
            ManualExpense,
            ManualIncome,
            ManualIncomeTaxPos,
            PensionFund,
            Pillar3a,
            Pillar3aPolice,
            Pillar3bPolice,
            RealEstate,
            VestedBenefit,
        ]

        for cls in classesToReset:
            cls.reset_allPlanValue(scenario)

        # 2. Step calculate planValue for each Month

        for period in MonthYear.create_range(
            startDate=Scenario.baseDate.nextMonth, endDate=Scenario.endDate
        ):
            # 3. Step calculate all manualPositions
            exe_manualIncomePlanning(period=period, scenario=scenario)
            exe_manualExpensePlanning(period=period, scenario=scenario)
