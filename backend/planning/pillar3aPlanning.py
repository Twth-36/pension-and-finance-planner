from backend.classes.pillar3a import Pillar3a
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.utils.mathFunctions import geometric12th
from backend.utils.monthYear import MonthYear


def exe_pillar3aPlanning(period: MonthYear, scenario: Scenario):

    # work through every object in instanceDic:
    for obj in Pillar3a.instanceDic.values():

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

        """handle 'manual' deposit"""
        deposit_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.deposit
        )

        if deposit_pos:
            # get Expense-Position
            depositExpense_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.depositExpense.planValue
            )

            depositExpense_pos.value -= deposit_pos.value
            new_pos.value += deposit_pos.value

            if deposit_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + deposit_pos.description
                else:
                    new_pos.description = deposit_pos.description

        """handle 'automatic' deposit"""
        depositAutomatic_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.depositAutomatic
        )

        if depositAutomatic_pos:
            # get Expense-Position
            depositExpense_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.depositExpense.planValue
            )

            depositExpense_pos.value -= depositAutomatic_pos.value
            new_pos.value += depositAutomatic_pos.value

            if depositAutomatic_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + depositAutomatic_pos.description
                else:
                    new_pos.description = depositAutomatic_pos.description

        """handle WEF"""
        WEF_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.WEF
        )
        if WEF_pos:
            # get Cashflow-Pos
            WEFCF_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.WEFCF.planValue
            )

            WEFCF_pos.value += min(WEF_pos.value, new_pos.value)
            new_pos.value -= min(WEF_pos.value, new_pos.value)
            if WEF_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + WEF_pos.description
                else:
                    new_pos.description = WEF_pos.description

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
