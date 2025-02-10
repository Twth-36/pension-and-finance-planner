


from router.freeAsset import *
from router.manualExpense import *
from router.manualIncome import *
from generalClasses import *
from router.pensionFund import *
from router.pillar3a import *
from router.realEstate import *

examplePlans = ["Verheiratetes Paar", "Paar in Konkubinat", "Alleinstehend"]
    

def examplePlanMarried():
    # Persons
    create_person("Andy")
    create_person("Lou")

    # Incomes
    create_manualIncome(name="Erwerbseinkommen Post", personName="Andy", baseValue=50000)
    create_manualIncome(name="Erwerbseinkommen SBB", personName="Lou", baseValue=80000)

    # Expenses
    create_manualExpense(name="Lebenshaltungskosten", baseValue=45000) #work on without personName

    # Free Assets
    create_freeAsset(name="Sparkonto UBS", personName="Andy", baseValue=40000)
    create_freeAsset(name="Sparkonto PostFinance", personName="Lou", baseValue=40000)
    create_freeAsset(name="Haushaltskonto Valiant", baseValue=10000)

    # PensionFund
    create_pensionFund(name="PK Post", personName="Andy", baseValue=450000)
    create_pensionFund(name="PK SBB", personName="Lou", baseValue=400000)

    # Pillar 3a
    create_pillar3a(name="Säule 3a Depot UBS", personName="Andy", baseValue=70000)
    create_pillar3aInsurance(name="Säule 3a Police AXA", personName="Lou", baseValue=90000)

    create_realEstate(name="EFH Biel", baseValue=80000)


    
    







