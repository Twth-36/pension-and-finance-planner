from backend.classes.credit import *
from backend.classes.freeAsset import *
from backend.classes.manualExpense import ManualExpense
from backend.classes.manualIncome import ManualIncome
from backend.classes.manualIncomeTaxPos import ManualIncomeTaxPos
from backend.classes.pensionFund import PensFundPayoutPos, PensionFund
from backend.classes.pillar3a import Pillar3a
from backend.classes.realEstate import *
from backend.classes.taxes import Taxes
from backend.classes.vestedBenefit import VestedBenefit


def examplePlanMarried():
    # Persons
    anna = Person.create(
        name="Anna", birth=MonthYear(month=11, year=1967), conf=Confession.ev_rev
    )
    bernd = Person.create(
        name="Bernd", birth=MonthYear(month=9, year=1966), conf=Confession.keine_andere
    )
    pensionDateAnna = MonthYear(month=11, year=2032)
    pensionDateBernd = MonthYear(month=9, year=2031)

    Scenario.endDate = MonthYear(month=12, year=2035)
    # Scenarios
    scenario = Scenario.create(
        name="Testszenario 1",
        description="Dies ist ein erstes Szenario welches zu Testzwecken dient.",
    )
    Scenario.create(name="Testzenario 2")

    # taxes
    Taxes.taxation = Taxation.together

    # Incomes
    incomeAnna = ManualIncome.create(
        name="Erwerbseinkommen Migros", person=anna, baseValue=6000
    )
    Planningposition(
        scenario=scenario, period=pensionDateAnna, value=0, description="Pensionierung"
    ).add_toList(incomeAnna.fixValue)

    incomeBernd = ManualIncome.create(
        name="Erwerbseinkommen Coop", person=bernd, baseValue=4000
    )
    Planningposition(
        scenario=scenario, period=pensionDateBernd, value=0, description="Pensionierung"
    ).add_toList(incomeBernd.fixValue)

    # Expenses
    ManualExpense.create(name="Lebenshaltungskosten", baseValue=3000)
    ManualExpense.create(name="Miete Zweitwohnung", baseValue=1000, person=anna)

    # Free Assets
    FreeAsset.create(name="Sparkonto UBS", person=anna, baseValue=100000)
    FreeAsset.create(name="Sparkonto PostFinance", person=bernd, baseValue=150000)
    FreeAsset.create(name="Haushaltskonto Valiant", baseValue=10000)

    # PensionFund
    pensFundAnna = PensionFund.create(
        name="PK Migros",
        person=anna,
        baseValue=450000,
        returnRate=1.5,
        baseSavingContribution=1500,
    )
    PensFundPayoutPos(
        scenario=scenario,
        period=pensionDateAnna,
        value=100,
        capitalPortion=50,
        conversionRate=6,
    ).add_toList(pensFundAnna.payout)
    Planningposition(scenario=scenario, period=pensionDateAnna, value=0).add_toList(
        pensFundAnna.savingContribution
    )

    pensFundBernd = PensionFund.create(
        name="PK Coop",
        person=bernd,
        baseValue=400000,
        returnRate=1,
        baseSavingContribution=1000,
        description="Kapitalbezug 50%",
    )
    PensFundPayoutPos(
        scenario=scenario,
        period=pensionDateBernd,
        value=100,
        capitalPortion=25,
        conversionRate=6.8,
        description="Kapitalbezug 25%",
    ).add_toList(pensFundBernd.payout)
    Planningposition(scenario=scenario, period=pensionDateBernd, value=0).add_toList(
        pensFundBernd.savingContribution
    )

    vestedBernd = VestedBenefit.create(
        name="Freizügigkeitsdepot Bernd",
        person=bernd,
        baseValue=100000,
        returnRate=3.5,
    )

    Planningposition(
        scenario=scenario,
        period=MonthYear(month=12, year=2030, description="Bezug Freizügigkeit"),
    ).add_toList(vestedBernd.payoutDate)

    # Pillar 3a
    Pillar3a.create(name="Säule 3a Depot UBS", person=anna, baseValue=70000)
    Pillar3a.create(name="Säule 3a Depot PostFinance", person=bernd, baseValue=80000)

    home = RealEstate.create(name="EFH in Biel", baseValue=1000000, maintCostRate=1)
    Planningposition(
        scenario=scenario,
        period=MonthYear(month=10, year=2027),
        value=10000,
        description="Renovation Badezimmer",
    ).add_toList(home.renovations)

    darlehen = Credit.create(
        name="Darlehen",
        person=anna,
        baseValue=20000,
    )
    Planningposition(
        scenario=scenario,
        period=MonthYear(month=2, year=2026),
        value=20000,
        description="Rückzahlung Darlehen",
    ).add_toList(darlehen.payback)

    Credit.create(
        name="Hypothek",
        baseValue=100000,
        endDate=MonthYear(month=8, year=2030),
        realEstate=home,
    )

    ManualIncomeTaxPos.create(
        name="Berufskosten Anna",
        Person=anna,
        baseValue=2000,
        type=TaxPositionType.deduction,
    )
    ManualIncomeTaxPos.create(
        name="Berufskosten Bernd",
        Person=bernd,
        baseValue=2000,
        type=TaxPositionType.deduction,
    )
