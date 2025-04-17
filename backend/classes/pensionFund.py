"""Class for PensionFund inclusive organising withdrawal as capital or pension"""

from pydantic import BaseModel, Field, field_validator
from typing import ClassVar, Optional, List
from .expense import *
from .income import *
from .planningposition import *
from .person import *


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
    capitalPortion: (
        float  # Portion OF THE WITHDRAWED pensioncapital which gets paid out as capital
    )
    conversionRate: float  # dt: Umwandlungssatz

    def update(
        self,
        list: List["PensFundPayoutPos"],
        new_scenario: Scenario = None,
        new_period: MonthYear = None,
        new_inDoc: bool = None,
        new_value: float = None,
        new_description: str = None,
        new_capitalPortion: float = None,
        new_conversionRate: float = None,
    ):

        # calling inherited function
        super().update(
            list=list,
            new_scenario=new_scenario,
            new_period=new_period,
            new_inDoc=new_inDoc,
            new_value=new_value,
            new_description=new_description,
        )

        # manage aditional attributes
        if new_capitalPortion is not None and new_capitalPortion != self.capitalPortion:
            self.capitalPortion = new_capitalPortion
        if new_conversionRate is not None and new_conversionRate != self.conversionRate:
            self.conversionRate = new_conversionRate


class PensionFund(BaseModel):
    # Object-attributes
    name: str
    person: Person
    baseValue: Optional[float] = 0
    fixValue: Optional[List[Planningposition]] = []  # overturns planning value
    planValue: Optional[List[Planningposition]] = []
    returnRate: Optional[float] = 0
    baseSavingContribution: float = 0
    savingContribution: Optional[List[Planningposition]] = (
        []
    )  # dt: Sparbeitrag (monthly)

    buyin: Optional[List[Planningposition]] = []
    buyinExpense: Optional[Expense] = None  # Expenseobject to make buyins

    payout: Optional[List[PensFundPayoutPos]] = []
    pensionIncome: Optional[Income] = None  # for payout as pension
    pensionCF: Optional[Cashflow] = None  # for capital payout

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    # Validation for unique name
    @field_validator("name", mode="after")
    @classmethod
    def check_uniquename(cls, name: str) -> str:
        if name == "":
            raise ValueError(f"May not be empty")
        if name in cls.instanceDic:
            raise ValueError(f"An object with name '{name}' already exists")
        return name

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} may not be negative")
        return baseValue

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "PensionFund":
        obj = cls.model_validate(data)  # Creation and validation
        cls.instanceDic[obj.name] = obj  # adding to instanceDic

        if obj.buyinExpense is None:
            param = {"name": "PK-Einkauf: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.buyinExpense = Expense.create(**param)

        if obj.pensionIncome is None:
            param = {"name": "PK-Rente: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.pensionIncome = Income.create(**param)

        if obj.pensionCF is None:
            param = {"name": "PK-Auszahlung: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.pensionCF = Cashflow.create(**param)

        return obj

    @classmethod
    def get_itemByName(cls, name: str) -> "PensionFund":
        return cls.instanceDic[name]

    def update_name(self, newname: str):
        self.__class__.check_uniquename(name=newname)
        self.__class__.instanceDic[newname] = self.__class__.instanceDic.pop(self.name)
        self.name = newname

    def delete_item(self):
        del self.__class__.instanceDic[self.name]


# rebuild model to ensure other classes are loaded
PensionFund.model_rebuild()
