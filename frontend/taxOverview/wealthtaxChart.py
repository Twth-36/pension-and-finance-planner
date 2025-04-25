import asyncio
from nicegui import ui


from backend.tax.taxproperties import Canton, Confession, Taxation
from backend.tax.wealthTax import clc_wealthTax


def clc_chartData(
    canton: Canton, place: str, taxation: Taxation, conf: Confession, childrenCnt: int
):
    minValue = 1
    maxValue = 1000001
    stp = int((maxValue - minValue) / 500)

    x = list(range(minValue, maxValue, stp))
    taxes = [
        [
            wlth,
            round(
                clc_wealthTax(
                    wealth=wlth,
                    canton=canton,
                    place=place,
                    taxation=taxation,
                    conf1=conf,
                    conf2=conf if taxation == Taxation.together else None,
                    childrenCnt=childrenCnt,
                )
            ),
        ]
        for wlth in x
    ]
    percTaxes = [[wlth, round(tax / wlth * 100, 2)] for wlth, tax in taxes]

    return taxes, percTaxes, stp


async def show_wealthTaxChart(
    canton: Canton,
    place: str,
    taxation: Taxation,
    conf: Confession,
    childrenCnt: int = 0,
):

    n = ui.notification(
        message="Computing...", spinner=True, type="ongoing", timeout=None
    )

    taxes, percTaxes, stp = await asyncio.to_thread(
        clc_chartData, canton, place, taxation, conf, childrenCnt
    )
    n.dismiss()

    # render the chart
    ui.echart(
        {
            "title": {
                "text": "Vermögenssteuer abhängig vom Reinvermögen",
                "subtext": "Der Grenzsteuersatz (%) wurde mit einer Schrittlänge von "
                + str(stp)
                + " approximiert.",
                "top": "5%",
            },
            "legend": {"top": "15%"},
            "grid": {"top": "25%", "containLabel": True},
            "tooltip": {"trigger": "axis"},
            "toolbox": {
                "show": True,
                "feature": {
                    "dataZoom": {},
                    "dataView": {},
                    "restore": {},
                },
            },
            "xAxis": {
                "type": "value",
                "axisLabel": {"formatter": "{value} CHF"},
            },
            "yAxis": [
                {
                    "type": "value",
                    "axisLabel": {"formatter": "{value} CHF"},
                },
                {
                    "type": "value",
                    "axisLabel": {"formatter": "{value} %"},
                },
            ],
            "series": [
                {
                    "name": "Vermögenssteuer",
                    "type": "line",
                    "data": taxes,
                    "showSymbol": False,
                    "itemStyle": {"color": "grey"},
                    "lineStyle": {"color": "grey"},
                    "areaStyle": {"color": "grey"},
                    "yAxisIndex": 0,
                },
                {
                    "name": "Vermögenssteuer (%)",
                    "type": "line",
                    "data": percTaxes,
                    "showSymbol": False,
                    "itemStyle": {"color": "black"},
                    "lineStyle": {"color": "black"},
                    "yAxisIndex": 1,
                },
            ],
        }
    ).classes("h-96")
