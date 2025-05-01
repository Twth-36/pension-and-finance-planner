import asyncio
from backend.classes.income import Income
from backend.classes.manualIncome import ManualIncome
from backend.classes.scenario import Scenario
from backend.utils.monthYear import MonthYear
from nicegui import ui


def get_rows(
    scenario: Scenario, months, title: str, dicsAsList: list, sumAgg: bool = True
):
    # create list of years
    years = sorted({m.year for m in months})

    titlerow = {"isTitle": True, "name": title, "person": None}
    for m in months:
        titlerow[m.dateToID()] = 0
    for y in years:
        titlerow[str(y) + "_FY"] = 0

    # initiallize rows
    rows = []

    # rows from ManualIncome and income
    for obj in dicsAsList:
        # make a row for each object
        row = {
            "isTitle": False,
            "name": obj.name,
            "person": obj.person.name if obj.person else None,
        }
        for y in years:
            agg_value = 0
            for m in months:
                if m.year == y:
                    # find according pos
                    pos = next(
                        (
                            p
                            for p in obj.planValue
                            if p.period == m and p.scenario == scenario
                        ),
                        None,
                    )
                    if pos:
                        row[m.dateToID()] = pos.value
                        row[m.dateToID() + "_tooltip"] = pos.description

                        # aggregation over year
                        if sumAgg == True:
                            agg_value += pos.value  # sum aggregation over year
                        elif sumAgg == False and m.month == 12:
                            agg_value = pos.value  # last value as aggregated

                        titlerow[
                            m.dateToID()
                        ] += pos.value  # sum aggregation over positions

            row[str(y) + "_FY"] = agg_value
            titlerow[str(y) + "_FY"] += agg_value  # sum aggregation over positions

        rows.append(row)

    # put titlerow in first posistion
    rows = [titlerow] + rows

    return rows
