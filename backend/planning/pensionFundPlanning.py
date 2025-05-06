from backend.classes.pensionFund import PensionFund
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.utils.mathFunctions import geometric12th
from backend.utils.monthYear import MonthYear


def exe_pensionFundPlanning(period: MonthYear, scenario: Scenario):

    # work through every object in instanceDic:
    for obj in PensionFund.instanceDic.values():

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

        """handle saving contribution"""
        # get last change of saving contribution
        savingContribution_pos = Planningposition.get_lastItem(
            startDate=Scenario.baseDate,
            endDate=period,
            scenario=scenario,
            list=obj.savingContribution,
        )

        if savingContribution_pos:  # case if once a new saving Contribution was made
            new_pos.value += savingContribution_pos.value

            if (
                savingContribution_pos.description
                and savingContribution_pos.period == period
            ):
                if new_pos.description:
                    new_pos.description += "; " + savingContribution_pos.description
                else:
                    new_pos.description = savingContribution_pos.description
        else:  # in cas still baseSavingContribution should be taken into account
            new_pos.value += obj.baseSavingContribution

        """ handle buyin"""
        buyin_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.buyin
        )
        if buyin_pos:  # case if buyin is planned in this period
            # get expense pos for buyin
            buyinExpense_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.buyinExpense.planValue
            )

            buyinExpense_pos.value -= buyin_pos.value
            new_pos.value += buyin_pos.value

            if buyin_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + buyin_pos.description
                else:
                    new_pos.description = buyin_pos.description

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

        """ handle monthly pension"""  # calculate obj.monthlyPensionPlanValue
        new_monthlyPensionPos = Planningposition(period=period, scenario=scenario)
        prev_monthlyPensionPos = Planningposition.get_item(
            period=period.nextMonth(-1),
            scenario=scenario,
            list=obj.monthlyPensionPlanValue,
        )
        if prev_monthlyPensionPos:
            new_monthlyPensionPos.value = prev_monthlyPensionPos.value
        else:
            new_monthlyPensionPos.value = 0

        new_monthlyPensionPos.add_toList(
            list=obj.monthlyPensionPlanValue
        )  # add help position for monthly payout to list

        """handle payout"""
        payout_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.payout
        )  # PensFundPayoutPos which inherits from PlanningPosition

        if payout_pos:
            """payout as capital part"""
            # get cashflowPos for payout
            payoutCF_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.pensionCF.planValue
            )

            payoutCF_pos.value += (
                new_pos.value
                * (payout_pos.value / 100)
                * (payout_pos.capitalPortion / 100)
            )  # value of pensionFund * how much one gets retired * how much gets withdrawed in capital

            """payout as monthly rent"""
            new_monthlyPensionPos.value += (
                new_pos.value
                * (payout_pos.value / 100)
                * (1 - payout_pos.capitalPortion / 100)
                * (payout_pos.conversionRate / 100)
                / 12
            )  # value of pensionFund * how much one gets retired * how much gets withdrawed in monthly pension * conversionRate

            new_pos.value = new_pos.value * (
                1 - payout_pos.value / 100
            )  # value of pensionFund * how much person stays in working life

            if payout_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + payout_pos.description
                else:
                    new_pos.description = payout_pos.description

            # adjust

        """finish monthly rent by adding value to incomePos"""
        # get income Position
        monthlyPensionIncome_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.pensionIncome.planValue
        )
        monthlyPensionIncome_pos.value += new_monthlyPensionPos.value

        # add new position planValue
        new_pos.add_toList(obj.planValue)
