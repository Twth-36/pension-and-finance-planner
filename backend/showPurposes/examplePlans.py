from backend.classes.credit import *
from backend.classes.freeAsset import *
from backend.classes.manualExpense import ManualExpense
from backend.classes.manualIncome import ManualIncome
from backend.classes.manualIncomeTaxPos import ManualIncomeTaxPos
from backend.classes.pensionFund import PensionFund
from backend.classes.pillar3a import Pillar3a
from backend.classes.realEstate import *


def examplePlanMarried():
    # Persons
    andy = Person.create(
        name="Andy", birth=MonthYear(month=11, year=1970), conf=Confession.ev_rev
    )
    lou = Person.create(
        name="Lou", birth=MonthYear(month=9, year=1972), conf=Confession.keine_andere
    )

    # Scenarios
    Scenario.create(name="Testszenario 1")
    Scenario.create(name="Testzenario 2")

    # Incomes
    ManualIncome.create(name="Erwerbseinkommen Post", person=andy, baseValue=8000)
    ManualIncome.create(name="Erwerbseinkommen SBB", person=lou, baseValue=4000)

    # Expenses
    ManualExpense.create(name="Lebenshaltungskosten", baseValue=45000)
    ManualExpense.create(name="Miete Zweitwohnung", baseValue=1000, person=lou)

    # Free Assets
    FreeAsset.create(name="Sparkonto UBS", person=andy, baseValue=100000)
    FreeAsset.create(name="Sparkonto PostFinance", person=lou, baseValue=150000)
    FreeAsset.create(name="Haushaltskonto Valiant", baseValue=10000)

    # PensionFund
    PensionFund.create(name="PK Post", person=andy, baseValue=450000)
    PensionFund.create(name="PK SBB", person=lou, baseValue=400000)

    # Pillar 3a
    Pillar3a.create(name="Säule 3a Depot UBS", person=andy, baseValue=70000)

    home = RealEstate.create(name="EFH", baseValue=1000000)

    Credit.create(
        name="Darlehen",
        person=andy,
        baseValue=20000,
    )
    Credit.create(
        name="Hypothek",
        baseValue=100000,
        endDate=MonthYear(month=8, year=2030),
        realEstate=home,
    )

    ManualIncomeTaxPos.create(
        name="Alleinstehendenabzug", baseValue=4000, type=TaxPositionType.deduction
    )
