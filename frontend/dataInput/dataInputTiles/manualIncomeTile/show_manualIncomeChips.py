from nicegui import ui
from backend.classes.monthYear import MonthYear
from backend.classes.manualIncome import ManualIncome
from frontend.utils import *


# chips:
def show_manualIncomeChips(card, manualIncome: ManualIncome, scenario: Scenario):
    card.clear()
    with card:
        with ui.row():
            # Chip for Renovation
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_manualIncomeChips(
                            card=card, manualIncome=manualIncome, scenario=scenario
                        )

                params_new = {
                    "planPosList": manualIncome.renovations,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt per wann die Renovation geplant ist",
                    "valueLabel": "Betrag",
                    "valueTooltip": "Betrag, welcher für die Renovation aufgewendet wird",
                }
                ui.chip(
                    text="Renovation",
                    icon="add",
                    color="blue",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_renovations = [
                    r for r in manualIncome.renovations if r.scenario == scenario
                ]
                for planPos in filtered_renovations:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(value=planPos.value)}",
                            color="blue",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": manualIncome.renovations,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt per wann die Renovation geplant ist",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Betrag, welcher für die Renovation aufgewendet wird",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: manualIncome.renovations.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for sale
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_manualIncomeChips(
                            card=card, manualIncome=manualIncome, scenario=scenario
                        )

                params_new = {
                    "planPosList": manualIncome.sale,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt des Verkaufs der Liegenschaft",
                    "valueLabel": "Verkaufserlös",
                    "valueTooltip": "Dieser Betrag wird dem freien Vermögen gutgeschrieben. Der Liegenschafts- und Steuerwert wird auf 0 gesetzt.",
                }
                ui.chip(
                    text="Verkauf",
                    icon="add",
                    color="indigo-3",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_sale = [p for p in manualIncome.sale if p.scenario == scenario]
                for planPos in filtered_sale:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(planPos.value)}",
                            color="indigo-3",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": manualIncome.sale,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt des Verkaufs der Liegenschaft",
                                    "valueLabel": "Verkaufserlös",
                                    "valueTooltip": "Dieser Betrag wird dem freien Vermögen gutgeschrieben. Der Liegenschafts- und Steuerwert wird auf 0 gesetzt.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: manualIncome.sale.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for purchase
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_manualIncomeChips(
                            card=card, manualIncome=manualIncome, scenario=scenario
                        )

                params_new = {
                    "planPosList": manualIncome.purchase,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt in welchem der Kauf der Liegenschaft oder einer Investition erfolgt",
                    "valueLabel": "Betrag",
                    "valueTooltip": "Dieser Betrag wird dem freien Vermögen abgezogen und dem Liegenschaftswert zugezählt. Denke daran allenfalls den Steuerwert anzupassen.",
                }
                ui.chip(
                    text="Kauf / Investition",
                    icon="add",
                    color="orange",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_purchase = [
                    p for p in manualIncome.purchase if p.scenario == scenario
                ]
                for planPos in filtered_purchase:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(planPos.value)}",
                            color="orange",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": manualIncome.purchase,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt in welchem der Kauf der Liegenschaft oder einer Investition erfolgt",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Dieser Betrag wird dem freien Vermögen abgezogen und dem Liegenschaftswert zugezählt. Denke daran allenfalls den Steuerwert anzupassen.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: manualIncome.purchase.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for new taxvalue
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_manualIncomeChips(
                            card=card, manualIncome=manualIncome, scenario=scenario
                        )

                params_new = {
                    "planPosList": manualIncome.taxValue,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Monat ab welchem der neue Steuerwert berücksichtigt werden soll.",
                    "valueLabel": "Steuerwert",
                    "valueTooltip": "Neuer Steuerwert zur Berechnung der Liegenschaftssteuer.",
                }
                ui.chip(
                    text="Neuer Steuerwert",
                    icon="add",
                    color="grey",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_taxValue = [
                    p for p in manualIncome.taxValue if p.scenario == scenario
                ]
                for planPos in filtered_taxValue:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(planPos.value)}",
                            color="grey",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": manualIncome.taxValue,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Monat ab welchem der neue Steuerwert berücksichtigt werden soll.",
                                    "valueLabel": "Steuerwert",
                                    "valueTooltip": "Neuer Steuerwert zur Berechnung der Liegenschaftssteuer.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: manualIncome.taxValue.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)
