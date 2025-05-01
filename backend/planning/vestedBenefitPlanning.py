from pandas import Period

from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.classes.vestedBenefit import VestedBenefit
from backend.utils.mathFunctions import geometric12th


def exe_vestedBenefitPlanning(period: Period, scenario: Scenario):

    # work through every object in instanceDic:
    for obj in VestedBenefit.instanceDic.values():

        # create new Planningposition for planValue
        new_pos = Planningposition(scenario=scenario, period=period)

        # find previous Planningposition planValue
        prev_pos = Planningposition.get_item(
            period=period.nextMonth(-1), scenario=scenario, list=obj.planValue
        )

        if prev_pos is None:  # case if first planningMonth
            new_pos.value = obj.baseValue
        else:
            new_pos.value = prev_pos.value

        """account returnRate"""
        new_pos.value += (
            new_pos.value * geometric12th(obj.returnRate) / 100
        )  # add monthly return

        """handle payout"""
        payoutDate_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.payoutDate
        )
        if payoutDate_pos:

            # get CF-position for payout
            payoutCF_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.payoutCF.planValue
            )
            payoutCF_pos.value += new_pos.value

            new_pos.value = 0

            # add description
            if payoutDate_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + payoutDate_pos.description
                else:
                    new_pos.description = payoutDate_pos.description

        # add new position planValue
        new_pos.add_toList(obj.planValue)
