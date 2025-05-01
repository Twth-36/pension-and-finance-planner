import asyncio
from backend.classes.cashflow import Cashflow
from backend.classes.credit import Credit
from backend.classes.expense import Expense
from backend.classes.income import Income
from backend.classes.incomeTaxPos import IncomeTaxPos
from backend.classes.manualExpense import ManualExpense
from backend.classes.manualIncome import ManualIncome
from backend.classes.manualIncomeTaxPos import ManualIncomeTaxPos
from backend.classes.pensionFund import PensionFund
from backend.classes.realEstate import RealEstate
from backend.classes.scenario import Scenario
from backend.classes.vestedBenefit import VestedBenefit
from backend.utils.monthYear import MonthYear
from nicegui import ui


from frontend.finPlan.grid.rowsGenerator import get_rows


async def show_finPlanGrid(scenario: Scenario):

    # create lists of month and years which are used in the planning
    months = MonthYear.create_range(
        startDate=Scenario.baseDate.nextMonth(), endDate=Scenario.endDate
    )
    years = sorted({m.year for m in months})

    columns_def = [
        # Zeilentitel
        {"field": "name", "headerName": "", "sortable": False, "filter": False},
        {
            "field": "person",
            "headerName": "",
            "sortable": False,
            "filter": False,
        },
    ] + [
        {
            # Column group for each year
            "headerName": y,
            "children": [
                {
                    "columnGroupShow": "closed",
                    "field": str(y) + "_FY",
                    "headerName": "FY",
                    "sortable": False,
                    "filter": False,
                    "type": ["numericColumn"],
                    # formatter to show 1000er
                    ":valueFormatter": 'params => params.value != null ? Math.round(params.value / 1000) : ""',
                }
            ]
            + [
                {
                    "columnGroupShow": "open",
                    "field": m.dateToID(),
                    "headerName": m.dateToString(),
                    "tooltipField": m.dateToID() + "_tooltip",
                    "sortable": False,
                    "filter": False,
                    "type": ["numericColumn"],
                    # formatter to show 1000er
                    ":valueFormatter": 'params => params.value != null ? Math.round(params.value / 1000) : ""',
                    # format blue if tooltip available
                    ":cellClassRules": {
                        "bg-blue-100": "data[colDef.tooltipField] != null",
                    },
                }
                for m in months
                if m.year == y
            ],
        }
        for y in years
    ]

    # calculate rows with asyncio since it needs time...
    n = ui.notification(
        message="Computing...", spinner=True, type="ongoing", timeout=None
    )
    # put rows together
    rows = []

    # incomeRows
    rows.extend(
        await asyncio.to_thread(
            get_rows,
            scenario,
            months,
            "Einkommen",
            list(ManualIncome.instanceDic.values()) + list(Income.instanceDic.values()),
        )
    )

    # expenseRows
    rows.extend(
        await asyncio.to_thread(
            get_rows,
            scenario,
            months,
            "Ausgaben",
            list(ManualExpense.instanceDic.values())
            + list(Expense.instanceDic.values()),
        )
    )
    rows.append({})  # add empty row

    # pensionFund rows
    rows.extend(
        await asyncio.to_thread(
            get_rows,
            scenario,
            months,
            "Pensionskassen",
            list(PensionFund.instanceDic.values()),
            False,
        )
    )

    # vestedBenefitRows
    rows.extend(
        await asyncio.to_thread(
            get_rows,
            scenario,
            months,
            "Freizügigkeitsguthaben",
            list(VestedBenefit.instanceDic.values()),
            False,
        )
    )

    # realEstateRows
    rows.extend(
        await asyncio.to_thread(
            get_rows,
            scenario,
            months,
            "Liegenschaften",
            list(RealEstate.instanceDic.values()),
            False,
        )
    )

    # credit-Rows
    rows.extend(
        await asyncio.to_thread(
            get_rows,
            scenario,
            months,
            "Kredite / Hypotheken",
            list(Credit.instanceDic.values()),
            False,
        )
    )
    rows.append({})  # add empty row

    # CF-rows
    rows.extend(
        await asyncio.to_thread(
            get_rows,
            scenario,
            months,
            "Cashflow",
            list(Cashflow.instanceDic.values()),
            True,
        )
    )
    rows.append({})  # add empty row

    # IncomeTaxPos-Rows
    rows.extend(
        await asyncio.to_thread(
            get_rows,
            scenario,
            months,
            "Steuerbares Einkommen",
            list(ManualIncomeTaxPos.instanceDic.values())
            + list(IncomeTaxPos.instanceDic.values()),
            True,
        )
    )
    rows.append({})  # add empty row

    filtered_rows = []
    for r in rows:
        # keep empty separators and title rows
        if not r or r.get("isTitle"):
            filtered_rows.append(r)
            continue
        # extract numeric values
        nums = [v for v in r.values() if isinstance(v, (int, float))]
        # keep rows with any non-zero numeric value
        if nums and any(v != 0 for v in nums):
            filtered_rows.append(r)

    n.dismiss()

    grid = (
        ui.aggrid(
            {
                "columnDefs": columns_def,
                "rowData": filtered_rows,
                "rowClassRules": {"font-bold": "data.isTitle"},  # makes bold if title
                "defaultColDef": {
                    "resizable": True,
                    "minWidth": 80,
                },
                "tooltipShowDelay": 0.5,
            },
        )
        .classes("w-full h-96 resize-y overflow-auto")
        .on("cellDoubleClicked", lambda event: print(event.args))
    )
