import asyncio
from nicegui import ui

from backend.classes.person import Person
from backend.classes.taxes import Taxes
from backend.tax.taxproperties import Confession, Taxation
from frontend.taxOverview.capPayoutTaxChart import show_capPayoutTaxChart
from frontend.taxOverview.incomeTaxChart import show_incomeTaxChart
from frontend.taxOverview.wealthTaxChart import show_wealthTaxChart


async def show_taxOverview(main_content):

    main_content.clear()
    with main_content:
        with ui.column():
            with ui.card().classes("q-pa-md border hover:!shadow-2xl"):
                ui.label("Berechnungsgrundlagen").classes("text-h6")
                with ui.grid(columns=2).classes("items-center"):
                    ui.label("Wohnkanton:").classes("text-body1 font-medium")
                    ui.label(Taxes.canton).classes(
                        "text-body1 font-semibold text-right"
                    )

                    ui.label("Wohnort:").classes("text-body1 font-medium")
                    ui.label(Taxes.place).classes("text-body1 font-semibold text-right")

                    conf = Confession.keine_andere
                    if next(iter(Person.instanceDic.values())):
                        conf = next(iter(Person.instanceDic.values())).conf
                    ui.label("Konfession:").classes("text-body1 font-medium")
                    ui.label(conf).classes("text-body1 font-semibold text-right")

                    ui.label("Besteuerung:").classes("text-body1 font-medium")
                    ui.label(Taxes.taxation).classes(
                        "text-body1 font-semibold text-right"
                    )
                    ui.label("Anzahl Kinder:").classes("text-body1 font-medium")
                    ui.label(Taxes.childrenCnt).classes(
                        "text-body1 font-semibold text-right"
                    )

        with ui.tabs().classes("w-full") as tabs:
            incomeTax = ui.tab("Einkommenssteuer")
            wealthTax = ui.tab("Vemögenssteuer")
            capTax = ui.tab("Kapitalauszahlungssteuer")
        with ui.tab_panels(tabs, value=incomeTax).classes("w-full"):
            with ui.tab_panel(incomeTax) as incomeTaxPanel:
                await show_incomeTaxChart(
                    canton=Taxes.canton,
                    place=Taxes.place,
                    taxation=Taxes.taxation,
                    conf=conf,
                    childrenCnt=Taxes.childrenCnt if Taxes.childrenCnt else 0,
                )

            with ui.tab_panel(wealthTax):
                await show_wealthTaxChart(
                    canton=Taxes.canton,
                    place=Taxes.place,
                    taxation=Taxes.taxation,
                    conf=conf,
                    childrenCnt=Taxes.childrenCnt if Taxes.childrenCnt else 0,
                )
            with ui.tab_panel(capTax):
                await show_capPayoutTaxChart(
                    canton=Taxes.canton,
                    place=Taxes.place,
                    taxation=Taxes.taxation,
                    conf=conf,
                    childrenCnt=Taxes.childrenCnt if Taxes.childrenCnt else 0,
                )
