from nicegui import ui
from backend.utils.monthYear import MonthYear
from backend.classes.realEstate import RealEstate
from backend.classes.scenario import Scenario
from frontend.utils import *
from frontend.utils.format import formatswiss
from frontend.utils.managePlanPos import dialog_planPos


# chips:
def show_realEstateChips(card, realEstate: RealEstate, scenario: Scenario):
    card.clear()
    with card:
        with ui.row():
            # Chip for Renovation
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_realEstateChips(
                            card=card, realEstate=realEstate, scenario=scenario
                        )

                params_new = {
                    "planPosList": realEstate.renovations,
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
                    r for r in realEstate.renovations if r.scenario == scenario
                ]
                for planPos in filtered_renovations:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(value=planPos.value)}",
                            color="blue",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": realEstate.renovations,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt per wann die Renovation geplant ist",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Betrag, welcher für die Renovation aufgewendet wird",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: realEstate.renovations.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for sale
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_realEstateChips(
                            card=card, realEstate=realEstate, scenario=scenario
                        )

                params_new = {
                    "planPosList": realEstate.sale,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt des Verkaufs der Liegenschaft",
                    "valueLabel": "Verkaufserlös",
                    "valueTooltip": "Dieser Betrag wird dem freien Vermögen gutgeschrieben. Der Liegenschafts-, Steuer- und Eigenmietwert wird auf 0 gesetzt. (Falls nichts anderes gepflegt)",
                }
                ui.chip(
                    text="Verkauf",
                    icon="add",
                    color="indigo-3",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_sale = [p for p in realEstate.sale if p.scenario == scenario]
                for planPos in filtered_sale:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(planPos.value)}",
                            color="indigo-3",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": realEstate.sale,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt des Verkaufs der Liegenschaft",
                                    "valueLabel": "Verkaufserlös",
                                    "valueTooltip": "Dieser Betrag wird dem freien Vermögen gutgeschrieben. Der Liegenschafts-, Steuer- und Eigenmietwert wird auf 0 gesetzt. (Falls nichts anderes gepflegt)",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: realEstate.sale.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for purchase
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_realEstateChips(
                            card=card, realEstate=realEstate, scenario=scenario
                        )

                params_new = {
                    "planPosList": realEstate.purchase,
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
                    p for p in realEstate.purchase if p.scenario == scenario
                ]
                for planPos in filtered_purchase:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(planPos.value)}",
                            color="orange",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": realEstate.purchase,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt in welchem der Kauf der Liegenschaft oder einer Investition erfolgt",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Dieser Betrag wird dem freien Vermögen abgezogen und dem Liegenschaftswert zugezählt. Denke daran allenfalls den Steuerwert anzupassen.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: realEstate.purchase.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for new taxvalue
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_realEstateChips(
                            card=card, realEstate=realEstate, scenario=scenario
                        )

                params_new = {
                    "planPosList": realEstate.taxFixValue,
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

                filtered_taxFixValue = [
                    p for p in realEstate.taxFixValue if p.scenario == scenario
                ]
                for planPos in filtered_taxFixValue:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(planPos.value)}",
                            color="grey",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": realEstate.taxFixValue,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Monat ab welchem der neue Steuerwert berücksichtigt werden soll.",
                                    "valueLabel": "Steuerwert",
                                    "valueTooltip": "Neuer Steuerwert zur Berechnung der Liegenschaftssteuer.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: realEstate.taxFixValue.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for new imputedRentalFixValue
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_realEstateChips(
                            card=card, realEstate=realEstate, scenario=scenario
                        )

                params_new = {
                    "planPosList": realEstate.imputedRentalFixValue,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Monat ab welchem der neue Eigenmietwert berücksichtigt werden soll. (Stichtag: Jahresende)",
                    "valueLabel": "Eigenmietwert",
                    "valueTooltip": "Neuer Eigenmietwert zur Berechnung des steuerbaren Einkommens.",
                }
                ui.chip(
                    text="Neuer Eigenmietwert",
                    icon="add",
                    color="green",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_imputedRentalFixValue = [
                    p
                    for p in realEstate.imputedRentalFixValue
                    if p.scenario == scenario
                ]
                for planPos in filtered_imputedRentalFixValue:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(planPos.value)}",
                            color="green",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": realEstate.imputedRentalFixValue,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Monat ab welchem der neue Eigenmietwert berücksichtigt werden soll. (Stichtag: Jahresende)",
                                    "valueLabel": "Eigenmietwert",
                                    "valueTooltip": "Neuer Eigenmietwert zur Berechnung des steuerbaren Einkommens.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: realEstate.imputedRentalFixValue.remove(
                                p
                            ),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)
