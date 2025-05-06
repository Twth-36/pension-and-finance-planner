from backend.classes.freeAsset import FreeAsset
from backend.classes.scenario import Scenario


def get_freeAssetRows(scenario: Scenario, months):
    # create list of years
    years = sorted({m.year for m in months})

    titlerow = {"isTitle": True, "name": "Freie Vermögenswerte", "person": None}
    for m in months:
        titlerow[m.dateToID()] = 0
    for y in years:
        titlerow[str(y) + "_FY"] = 0

    # initiallize rows
    rows = []

    liqRow = {"isTitle": False, "name": "Liquiditätsreserve", "person": None}
    for y in years:
        agg_value = 0
        for m in months:
            if m.year == y:
                # find according pos
                pos = next(
                    (
                        p
                        for p in FreeAsset.planValueLiq
                        if p.period == m and p.scenario == scenario
                    ),
                    None,
                )
                if pos:
                    liqRow[m.dateToID()] = pos.value

                    if m.month == 12:
                        agg_value = pos.value  # last value as aggregated

                    titlerow[
                        m.dateToID()
                    ] += pos.value  # sum aggregation over positions

        liqRow[str(y) + "_FY"] = agg_value
        titlerow[str(y) + "_FY"] += agg_value  # sum agg

    rows.append(liqRow)

    investCapRow = {"isTitle": False, "name": "Investiertes Kapital", "person": None}
    for y in years:
        agg_value = 0
        for m in months:
            if m.year == y:
                # find according pos
                pos = next(
                    (
                        p
                        for p in FreeAsset.planValueInvestCap
                        if p.period == m and p.scenario == scenario
                    ),
                    None,
                )
                if pos:
                    investCapRow[m.dateToID()] = pos.value

                    if m.month == 12:
                        agg_value = pos.value  # last value as aggregated

                    titlerow[
                        m.dateToID()
                    ] += pos.value  # sum aggregation over positions

        investCapRow[str(y) + "_FY"] = agg_value
        titlerow[str(y) + "_FY"] += agg_value  # sum agg

    rows.append(investCapRow)

    # put titlerow in first posistion
    rows = [titlerow] + rows

    return rows
