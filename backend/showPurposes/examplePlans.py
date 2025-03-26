


from classes.freeAsset import *
from classes.manualExpense import *
from classes.manualIncome import *
from generalClasses import *
from classes.pensionFund import *
from classes.pillar3a import *
from classes.realEstate import *

examplePlans = ["Verheiratetes Paar", "Paar in Konkubinat", "Alleinstehend"]
    

def examplePlanMarried():
    # Persons
    Person.create("Andy")
    Person.create("Lou")

    # Incomes
    ManualIncome.create(name="Erwerbseinkommen Post", personName="Andy", baseValue=50000)
    ManualIncome.create(name="Erwerbseinkommen SBB", personName="Lou", baseValue=80000)

    # Expenses
    ManualExpense.create(name="Lebenshaltungskosten", baseValue=45000) #work on without personName

    # Free Assets
    FreeAsset.create(name="Sparkonto UBS", personName="Andy", baseValue=40000)
    FreeAsset.create(name="Sparkonto PostFinance", personName="Lou", baseValue=40000)
    FreeAsset.create(name="Haushaltskonto Valiant", baseValue=10000)

    # PensionFund
    PensionFund.create(name="PK Post", personName="Andy", baseValue=450000)
    PensionFund.create(name="PK SBB", personName="Lou", baseValue=400000)

    # Pillar 3a
    Pillar3a.create(name="Säule 3a Depot UBS", personName="Andy", baseValue=70000)
    Pillar3aInsurance.create(name="Säule 3a Police AXA", personName="Lou", baseValue=90000)

    RealEstate.create(name="EFH Biel", baseValue=80000)


    
    







