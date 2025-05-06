from backend.classes.credit import Credit
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.utils.monthYear import MonthYear


def exe_creditPlanning(period: MonthYear, scenario: Scenario):

    # work through every object in instanceDic:
    for obj in Credit.instanceDic.values():

        # create new Planningposition for planValue
        new_pos = Planningposition(scenario=scenario, period=period)

        # find previous Planningposition planValue
        prev_pos = Planningposition.get_item(
            period=period.nextMonth(-1), scenario=scenario, list=obj.planValue
        )

        if prev_pos is None:  # case if first planningMonth
            new_pos.value = -obj.baseValue
        else:
            new_pos.value = prev_pos.value

        """handle payback"""
        payback_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.payback
        )
        if payback_pos:

            # get CF-position for payback
            paybackCF_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.paybackCF.planValue
            )
            paybackCF_pos.value -= payback_pos.value

            new_pos.value += payback_pos.value
            # add description
            if payback_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + payback_pos.description
                else:
                    new_pos.description = payback_pos.description

        """handle increase"""
        increase_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.increase
        )
        if increase_pos:

            # get CF-position for increase
            increaseCF_pos = Planningposition.get_item(
                period=period, scenario=scenario, list=obj.increaseCF.planValue
            )
            increaseCF_pos.value += increase_pos.value

            new_pos.value -= increase_pos.value
            # add description
            if increase_pos.description:
                if new_pos.description:
                    new_pos.description += "; " + increase_pos.description
                else:
                    new_pos.description = increase_pos.description

        """handle interestpos"""
        # get last change of interestRate
        interestRate_pos = Planningposition.get_lastItem(
            startDate=Scenario.baseDate,
            endDate=period,
            scenario=scenario,
            list=obj.interestRate,
        )
        # get Expense-position for interestRate
        interestExpense_pos = Planningposition.get_item(
            period=period, scenario=scenario, list=obj.interestExpense.planValue
        )
        if interestRate_pos:  # this mean once the interestRate was changed

            interestExpense_pos.value += (
                new_pos.value * interestRate_pos.value / 100 / 12
            )

            # add description
            if (
                interestRate_pos.description and interestRate_pos.period == period
            ):  # only if change just happened
                if interestExpense_pos.description:
                    interestExpense_pos.description += (
                        "; " + interestRate_pos.description
                    )
                else:
                    interestExpense_pos.description = interestRate_pos.description
        else:  # account base Interst Rate if never new interestRate was taken
            interestExpense_pos.value += new_pos.value * obj.baseInterestRate / 100 / 12

        # add new position planValue
        new_pos.add_toList(obj.planValue)
