import asyncio
from nicegui import ui


from backend.tax.capPayoutTax import clc_capPayoutTax
from backend.tax.taxproperties import Canton, Confession, Taxation


def clc_chartData(
    canton: Canton, place: str, taxation: Taxation, conf: Confession, childrenCnt: int
):
    minValue = 1
    maxValue = 500001
    stp = int((maxValue - minValue) / 500)

    x = list(range(minValue, maxValue, stp))
    taxes = [
        [
            payout,
            round(
                clc_capPayoutTax(
                    payoutValue=payout,
                    canton=canton,
                    place=place,
                    taxation=taxation,
                    conf1=conf,
                    conf2=conf if taxation == Taxation.together else None,
                    childrenCnt=childrenCnt,
                )
            ),
        ]
        for payout in x
    ]
    percTaxes = [[payout, round(tax / payout * 100, 2)] for payout, tax in taxes]

    marginTaxes = [
        [payout, round((tax - tax_prev) / stp * 100, 2)]
        for (payout_prev, tax_prev), (payout, tax) in zip(taxes, taxes[1:])
    ]
    return taxes, percTaxes, marginTaxes, stp


async def show_capPayoutTaxChart(
    canton: Canton,
    place: str,
    taxation: Taxation,
    conf: Confession,
    childrenCnt: int = 0,
):

    n = ui.notification(
        message="Computing...", spinner=True, type="ongoing", timeout=None
    )

    taxes, percTaxes, marginTaxes, stp = await asyncio.to_thread(
        clc_chartData, canton, place, taxation, conf, childrenCnt
    )
    n.dismiss()

    # render the chart
    ui.echart(
        {
            "title": {
                "text": "Kapitalauszahlungssteuer abhängig vom Auszahlungsbetrag",
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
                    "name": "Kapitalauszahlungssteuer",
                    "type": "line",
                    "data": taxes,
                    "showSymbol": False,
                    "itemStyle": {"color": "grey"},
                    "lineStyle": {"color": "grey"},
                    "areaStyle": {"color": "grey"},
                    "yAxisIndex": 0,
                },
                {
                    "name": "Kapitalauszahlungssteuer (%)",
                    "type": "line",
                    "data": percTaxes,
                    "showSymbol": False,
                    "itemStyle": {"color": "black"},
                    "lineStyle": {"color": "black"},
                    "yAxisIndex": 1,
                },
                {
                    "name": "Grenzsteuer (%)",
                    "type": "line",
                    "data": marginTaxes,
                    "showSymbol": False,
                    "itemStyle": {"color": "black"},
                    "lineStyle": {"type": "dashed", "color": "black"},
                    "yAxisIndex": 1,
                },
            ],
        }
    ).classes("h-96")
