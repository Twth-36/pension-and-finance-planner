""" Class for PensionFund inclusive organising withdrawal as capital or pension """

from pydantic import BaseModel, Field, field_validator
from typing import ClassVar, Optional, List
from classes.expense import *
from classes.income import *
from utils.nameManager import *
from planningposition import *
from person import *


class PensFundPayoutPos(Planningposition):
    # extends Planningposition with more variable
    """
    Inherited attributes:
        scenario: Scenario
        period: MonthYear
        value: Optional[float] = 0
        inDoc: Optional[bool] = False
        description: Optional[str] = None
    """
    withdrawalPortion: float # Portion which gets withdrawed as part of a (partly-)Pension
    capitalPortion: float # Portion OF THE WITHDRAWED pensioncapital which gets paid out as capital
    conversionRate: float # dt: Umwandlungssatz

class PensionFund(BaseModel):
    # Object-attributes
    name: str
    person: Person
    baseValue: float
    fixValue: Optional[List[Planningposition]] = [] #overturns planning value
    planValue: Optional[List[Planningposition]] = []
    returnRate: Optional[List[Planningposition]] = []
    savingContribution: Optional[List[Planningposition]] = [] #dt: Sparbeitrag (monthly)
    
    buyin: Optional[List[Planningposition]] = []
    buyinExpense: Optional[Expense] = None #Expenseobject to make buyins
    
    payout:  Optional[List[PensFundPayoutPos]] = []
    pensionIncome: Optional[Income] = None # for payout as pension
    pensionCF: Optional[Cashflow] = None # for capital payout

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator('baseValue', mode='after')  
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f'{baseValue} is strict smaller than 0')
        return baseValue 
    
    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "PensionFund":
        obj = cls.model_validate(data) #Creation and validation
        obj.name = generate_uniqueName(obj.name, cls.instanceDic) #generate unique name
        cls.instanceDic[obj.name] = obj #adding to instanceDic

        #if no pensionIncome-object is assigned -> generate one
        if obj.pensionIncome is None:
            obj.pensionIncome = Income.create(name="Rente - " + obj.name, person=obj.person, taxablePortion=1)
        
        return obj
    
