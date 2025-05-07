from backend.classes.cashflow import Cashflow
from backend.classes.credit import Credit
from backend.classes.expense import Expense
from backend.classes.freeAsset import FreeAsset
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


def copyAllFromScenario(new_scenario: Scenario, src_scenario: Scenario):
    classes = [
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

    for cls in classes:
        cls.copy_toNewScenario(new_scenario=new_scenario, src_scenario=src_scenario)
