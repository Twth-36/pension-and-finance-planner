from backend.classes.pillar3bPolice import Pillar3bPolice
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario

from backend.utils.monthYear import MonthYear
from backend.utils.payFrequency import PayFrequency


def exe_pillar3bPolicePlanning(period: MonthYear, scenario: Scenario):

    # work through every object in instanceDic:
    for obj in Pillar3bPolice.instanceDic.values():

        # create new Planningposition for planValue
        new_pos = Planningposition(scenario=scenario, period=period)

        # check if current period is strict smaller than payoutdate
        if (period.year < obj.payoutDate.year) or (
            period.year == obj.payoutDate.year and period.month < obj.payoutDate.month
        ):

            """calculate current value"""
            # calculate Rückkaufwert by cumulating deposits + baseValue
            if obj.depositFreq == PayFrequency.M:
                new_pos.value = (
                    obj.baseValue
                    + MonthYear.months_diff(startDate=Scenario.baseDate, endDate=period)
                    * obj.deposit
                )
            else:  # if yearly payment
                new_pos.value = (
                    obj.baseValue
                    + MonthYear.months_diff(startDate=Scenario.baseDate, endDate=period)
                    * obj.deposit
                    / 12
                )

            """handle deposit"""

            depositExpense_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.depositExpense.planValue
            )

            if obj.depositFreq == PayFrequency.M:
                depositExpense_pos.value -= obj.deposit

            elif (
                obj.depositFreq == PayFrequency.Y
                and period.month == obj.payoutDate.month
            ):
                depositExpense_pos.value -= obj.deposit
        else:  # case if current period is after payoutdate
            new_pos.value = 0

            """handle pension"""
            # get IncomePosition
            pensionIncome_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.pensionIncome.planValue
            )
            pensionIncome_pos.value += obj.expPensionValue

        """handle payout"""
        if period == obj.payoutDate:
            # get CF position
            payoutCF_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.payoutCF.planValue
            )
            payoutCF_pos.value += obj.expPayoutValue

        # add new position planValue
        new_pos.add_toList(obj.planValue)
