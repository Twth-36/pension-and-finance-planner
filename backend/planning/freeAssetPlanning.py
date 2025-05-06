from backend.classes.cashflow import Cashflow
from backend.classes.freeAsset import FreeAsset
from backend.classes.planningposition import Planningposition
from backend.classes.scenario import Scenario
from backend.utils.mathFunctions import geometric12th
from backend.utils.monthYear import MonthYear


def exe_freeAssetIncomePlanning(period: MonthYear, scenario: Scenario):

    # find incomePos
    returnIncome_pos = Planningposition.get_item(
        period=period, scenario=scenario, list=FreeAsset.returnIncome.planValue
    )

    # find previous Planningposition planValue of invested Cap
    prevInvestCap_pos = Planningposition.get_item(
        period=period.nextMonth(-1),
        scenario=scenario,
        list=FreeAsset.planValueInvestCap,
    )

    if (
        prevInvestCap_pos is None
    ):  # case if first planningMonth then sum of freeAsset - liqRes
        returnIncome_pos.value += (
            max(
                0,
                sum(freeAsset.baseValue for freeAsset in FreeAsset.instanceDic.values())
                - FreeAsset.liqRes,
            )
            * geometric12th(FreeAsset.returnRateInvestCap)
            / 100
        )
    else:
        returnIncome_pos.value += (
            prevInvestCap_pos.value * geometric12th(FreeAsset.returnRateInvestCap) / 100
        )


def exe_completeFreeAssets(period: MonthYear, scenario: Scenario):
    newLiq_pos = Planningposition(scenario=scenario, period=period)
    newInvestCap_pos = Planningposition(scenario=scenario, period=period)

    prevLiq_pos = Planningposition.get_item(
        period=period.nextMonth(-1), scenario=scenario, list=FreeAsset.planValueLiq
    )
    prevInvestCap_pos = Planningposition.get_item(
        period=period.nextMonth(-1),
        scenario=scenario,
        list=FreeAsset.planValueInvestCap,
    )

    if prevLiq_pos is None:
        newLiq_pos.value = 0
    else:
        newLiq_pos.value = prevLiq_pos.value

    if prevInvestCap_pos is None:
        newInvestCap_pos.value = sum(
            obj.baseValue for obj in FreeAsset.instanceDic.values()
        )
    else:
        newInvestCap_pos.value = prevInvestCap_pos.value

    # add all Cashflows
    for CFobj in Cashflow.instanceDic.values():
        CFpos = Planningposition.get_item(
            period=period, scenario=scenario, list=CFobj.planValue
        )
        newInvestCap_pos.value += CFpos.value

    # manage liqRes
    if newInvestCap_pos.value < 0:  # take from Liqres if <0
        newInvestCap_pos.value += max(0, min(newLiq_pos.value, -newInvestCap_pos.value))
        newLiq_pos.value -= max(0, min(newLiq_pos.value, -newInvestCap_pos.value))
    elif newLiq_pos.value < FreeAsset.liqRes:  # if LiqRes is smaller than planned
        newLiq_pos.value += max(
            0, min(FreeAsset.liqRes - newLiq_pos.value, newInvestCap_pos.value)
        )
        newInvestCap_pos.value -= max(
            0, min(FreeAsset.liqRes - newLiq_pos.value, newInvestCap_pos.value)
        )

    newInvestCap_pos.add_toList(FreeAsset.planValueInvestCap)
    newLiq_pos.add_toList(FreeAsset.planValueLiq)
