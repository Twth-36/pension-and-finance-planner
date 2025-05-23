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


class PensionFund(Planningobject):
    # Object-attributes
    baseValue: Optional[float] = 0
    fixValue: Optional[List[Planningposition]] = []  # overturns planning value
    returnRate: Optional[float] = 0
    baseSavingContribution: float = 0
    savingContribution: Optional[List[Planningposition]] = (
        []
    )  # dt: Sparbeitrag (monthly)

    buyin: Optional[List[Planningposition]] = []
    buyinExpense: Optional[Expense] = None  # Expenseobject to make buyins

    WEF: Optional[List[Planningposition]] = []
    WEFCF: Optional[Cashflow] = None

    payout: Optional[List[PensFundPayoutPos]] = []
    monthlyPensionPlanValue: Optional[List[Planningposition]] = (
        []
    )  # help-variable to calculate the monthly pension
    pensionIncome: Optional[Income] = None  # for payout as pension
    pensionCF: Optional[Cashflow] = None  # for capital payout

    # Class-attributes
    instanceDic: ClassVar[dict] = {}

    # Validation non-negative baseValue
    @field_validator("baseValue", mode="after")
    @classmethod
    def is_nonNegative(cls, baseValue: float) -> float:
        if baseValue < 0:
            raise ValueError(f"{baseValue} may not be negative")
        return baseValue

    @field_validator("buyinExpense", mode="before")
    @classmethod
    def _load_buyinExpense(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Expense.get_itemByName(v["name"])
        return v

    @field_validator("pensionIncome", mode="before")
    @classmethod
    def _load_pensionIncome(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Income.get_itemByName(v["name"])
        return v

    @field_validator("WEFCF", mode="before")
    @classmethod
    def _load_WEFCF(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Cashflow.get_itemByName(v["name"])
        return v

    @field_validator("pensionCF", mode="before")
    @classmethod
    def _load_pensionCF(cls, v):
        """
        If loading from JSON: when v is a dict like {"name": "..."},
        replace it with the existing instance
        (avoiding a duplicate‐name validation error).
        Otherwise (v is already a object or None), return it unchanged.
        """
        if isinstance(v, dict):
            return Cashflow.get_itemByName(v["name"])
        return v

    # Create new object with validation and adding to instanceDic
    @classmethod
    def create(cls, **data) -> "PensionFund":
        obj = super().create(**data)  # Creation in Planningobjectclass

        if obj.buyinExpense is None:
            param = {"name": "PK-Einkauf: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.buyinExpense = Expense.create(**param)

        if obj.WEFCF is None:
            param = {"name": "WEF: " + obj.name, "taxablePortion": 100}
            if obj.person:
                param["person"] = obj.person
            obj.WEFCF = Cashflow.create(**param)

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

    # overwrite super-function since not only planValue needs to be reset
    def reset_planValue(self, scenario: Scenario):
        # delets all planValue of an object with a specific scenario
        if not self.planValue:
            return
        super().reset_planValue(
            scenario=scenario
        )  # call super-function for resetting planValue

        # additionally reset monthlyPensionPlanValue
        self.monthlyPensionPlanValue = [
            p for p in self.monthlyPensionPlanValue if p.scenario != scenario
        ]

    @classmethod
    def copy_toNewScenario(cls, new_scenario: Scenario, src_scenario: Scenario):
        for obj in cls.instanceDic.values():

            # all lists with planValue where the scenario needs to be dublicated
            lists = [
                obj.planValue,
                obj.fixValue,
                obj.savingContribution,
                obj.buyin,
                obj.WEF,
            ]

            # duplicates all scenario related fields to a newscenario
            for planPosList in lists:
                for pos in planPosList:
                    if pos.scenario == src_scenario:
                        Planningposition(
                            scenario=new_scenario,
                            period=pos.period,
                            value=pos.value,
                            inDoc=pos.inDoc,
                            description=pos.description,
                        ).add_toList(planPosList)

            # treat payout seperatly since of class PensFundPayoutPos
            for pos in obj.payout:
                if pos.scenario == src_scenario:
                    PensFundPayoutPos(
                        scenario=new_scenario,
                        period=pos.period,
                        value=pos.value,
                        capitalPortion=pos.capitalPortion,
                        conversionRate=pos.conversionRate,
                        inDoc=pos.inDoc,
                        description=pos.description,
                    ).add_toList(obj.payout)


# rebuild model to ensure other classes are loaded
PensionFund.model_rebuild()
