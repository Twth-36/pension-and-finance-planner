from typing import List
from backend.classes.freeAsset import FreeAsset
from backend.planning.cashflowPlanning import exe_cashflowPlanning
from backend.planning.creditPlanning import exe_creditPlanning
from backend.planning.expensePlanning import (
    exe_completeExpensePlanning,
    exe_expensePlanning,
    exe_manualExpensePlanning,
)
from backend.planning.freeAssetPlanning import (
    exe_completeFreeAssets,
    exe_freeAssetIncomePlanning,
)
from backend.planning.incomePlanning import (
    exe_completeIncomePlanning,
    exe_incomePlanning,
    exe_manualIncomePlanning,
)
from backend.planning.incomeTaxPosPlanning import (
    exe_completeIncomeTaxPosPlanning,
    exe_incomeTaxPosPlanning,
    exe_manualIncomeTaxPosPlanning,
)

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
from backend.planning.pensionFundPlanning import exe_pensionFundPlanning
from backend.planning.pillar3aPlanning import exe_pillar3aPlanning
from backend.planning.pillar3aPolicePlanning import exe_pillar3aPolicePlanning
from backend.planning.pillar3bPolicePlanning import exe_pillar3bPolicePlanning
from backend.planning.realEstatePlanning import exe_realEstatePlanning
from backend.planning.taxesPlanning import exe_clcCapPayoutTax, exe_clcIncomeTax
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
            FreeAsset,
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

            # 5. Step calculate wealth-related position except freeAssets
            exe_realEstatePlanning(period=period, scenario=scenario)
            exe_creditPlanning(period=period, scenario=scenario)
            exe_pensionFundPlanning(period=period, scenario=scenario)
            exe_vestedBenefitPlanning(period=period, scenario=scenario)
            exe_pillar3aPlanning(period=period, scenario=scenario)
            exe_pillar3aPolicePlanning(period=period, scenario=scenario)
            exe_pillar3bPolicePlanning(period=period, scenario=scenario)

            # 6. Step calculate income from invested capital
            exe_freeAssetIncomePlanning(period=period, scenario=scenario)

            # 7. Step summarize (manual)Income, (manual)Expense and freeAssets
            exe_completeExpensePlanning(period=period, scenario=scenario)
            exe_completeIncomePlanning(period=period, scenario=scenario)
            exe_completeFreeAssets(period=period, scenario=scenario)

            # 8. Step summarize incomeTaxPos from Income and Expense and manualIncomeTaxPos
            exe_manualIncomeTaxPosPlanning(period=period, scenario=scenario)
            exe_completeIncomeTaxPosPlanning(period=period, scenario=scenario)

            # 9. STep calculate Taxes if 12. month
            if period.month == 12:
                exe_clcIncomeTax(period=period, scenario=scenario)
                exe_clcCapPayoutTax(period=period, scenario=scenario)

                # repeat these function after taxCalc:
                exe_completeExpensePlanning(period=period, scenario=scenario)
                exe_completeIncomePlanning(period=period, scenario=scenario)
                FreeAsset.reset_planValue(period=period, scenario=scenario)
                exe_completeFreeAssets(period=period, scenario=scenario)
