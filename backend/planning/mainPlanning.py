from typing import List
from backend.planning.cashflowPlanning import exe_cashflowPlanning
from backend.planning.creditPlanning import exe_creditPlanning
from backend.planning.expensePlanning import exe_expensePlanning
from backend.planning.incomePlanning import exe_incomePlanning
from backend.planning.incomeTaxPosPlanning import exe_incomeTaxPosPlanning
from backend.planning.manualExpensePlanning import exe_manualExpensePlanning
from backend.planning.manualIncomePlanning import exe_manualIncomePlanning
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
from backend.planning.manualIncomeTaxPosPlanning import exe_manualIncomeTaxPosPlanning
from backend.planning.pensionFundPlanning import exe_pensionFundPlanning
from backend.planning.realEstatePlanning import exe_realEstatePlanning
from backend.planning.vestedBenefitPlanning import exe_vestedBenefitPlanning
from backend.utils.monthYear import MonthYear


def exe_mainPlanning(scenarios: List[Scenario] = None, delObjects: bool = False):

    if scenarios is None:
        scenarios = [
            sc for sc in Scenario.instanceDic.values()
        ]  # if scenarios is not given as Argument make list with all scnearios

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
            startDate=Scenario.baseDate.nextMonth(), endDate=Scenario.endDate
        ):

            # 3. Step prepare planValue for Income, Expense, Cashflow
            exe_incomePlanning(period=period, scenario=scenario)
            exe_expensePlanning(period=period, scenario=scenario)
            exe_cashflowPlanning(period=period, scenario=scenario)
            exe_incomeTaxPosPlanning(period=period, scenario=scenario)

            # 4. Step calculate all manualPositions
            exe_manualIncomePlanning(period=period, scenario=scenario)
            exe_manualExpensePlanning(period=period, scenario=scenario)
            # exe_manualIncomeTaxPosPlanning(period=period, scenario=scenario) needs to be corrected such that only in december calculated

            # 5. Step calculate wealth-related position except freeAssets
            exe_realEstatePlanning(period=period, scenario=scenario)
            exe_creditPlanning(period=period, scenario=scenario)
            exe_pensionFundPlanning(period=period, scenario=scenario)
            exe_vestedBenefitPlanning(period=period, scenario=scenario)
