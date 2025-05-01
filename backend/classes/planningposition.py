"""Class for general planningposition"""

from pydantic import BaseModel
from ..utils.monthYear import MonthYear
from typing import Optional
from .scenario import *


class Planningposition(BaseModel):
    scenario: Scenario
    period: MonthYear
    value: Optional[float] = 0
    inDoc: Optional[bool] = False
    description: Optional[str] = None

    def is_inList(self, list: List["Planningposition"]) -> bool:
        return any(
            p.scenario.name == self.scenario.name and p.period == self.period
            for p in list
        )

    def add_toList(self, list: List["Planningposition"]):
        if self.is_inList(list):
            raise ValueError(
                f"Planningposition for this scenario and period exists already."
            )
        list.append(self)

    def update(
        self,
        list: List["Planningposition"],
        new_scenario: Scenario = None,
        new_period: MonthYear = None,
        new_inDoc: bool = None,
        new_value: float = None,
        new_description: str = None,
    ):
        if self.scenario != new_scenario or self.period != new_period:
            tmp_planPos = Planningposition(
                scenario=new_scenario or self.scenario,
                period=new_period or self.period,
            )
            if tmp_planPos.is_inList(list):
                raise ValueError(
                    f"Planningposition for this scenario and period exists already."
                )
            if new_scenario is not None and new_scenario != self.scenario:
                self.scenario = new_scenario
            if new_period is not None and new_period != self.period:
                self.period = new_period

        if new_value is not None and new_value != self.value:
            self.value = new_value
        if new_inDoc is not None and new_inDoc != self.inDoc:
            self.inDoc = new_inDoc
        if new_description is not None and new_description != self.description:
            self.description = new_description

    @classmethod
    def get_item(
        cls, period: MonthYear, scenario: Scenario, list: List["Planningposition"]
    ):
        for p in list:
            if p.scenario.name == scenario.name and p.period == period:
                return p

        return None

    @classmethod
    def get_lastItem(
        cls,
        startDate: MonthYear,
        endDate: MonthYear,
        scenario: Scenario,
        list: list["Planningposition"],
    ):
        currentDate = endDate
        while currentDate.year >= startDate.year or (
            currentDate.month >= startDate.month and currentDate == startDate.year
        ):

            pos = Planningposition.get_item(
                period=currentDate, scenario=scenario, list=list
            )
            if pos is not None:
                return pos
            else:
                currentDate = currentDate.nextMonth(-1)

        return None
