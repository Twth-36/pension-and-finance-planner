from nicegui import ui
from backend.classes.credit import Credit, Person
from backend.classes.monthYear import MonthYear
from backend.classes.scenario import Scenario
from frontend.utils.format import formatswiss
from frontend.utils.managePlanPos import dialog_planPos


# chips:
def show_creditChips(card, credit: Credit, scenario: Scenario):
    card.clear()
    with card:
        with ui.row():
            # Chip for payback
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_creditChips(card=card, credit=credit, scenario=scenario)

                params_new = {
                    "planPosList": credit.payback,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt per wann eine Amortisation erfolgt",
                    "valueLabel": "Betrag",
                    "valueTooltip": "Betrag, welcher amortisiert wird",
                }
                ui.chip(
                    text="Amortisation",
                    icon="add",
                    color="blue",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_payback = [p for p in credit.payback if p.scenario == scenario]
                for planPos in filtered_payback:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(value=planPos.value)}",
                            color="blue",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": credit.payback,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt per wann eine Amortisation erfolgt",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Betrag, welcher amortisiert wird",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: credit.payback.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for increase of the credit
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_creditChips(card=card, credit=credit, scenario=scenario)

                params_new = {
                    "planPosList": credit.increase,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt per wann eine Krediterhöhung erfolgt",
                    "valueLabel": "Betrag",
                    "valueTooltip": "Betrag welcher zusätzlich als Kredit aufgenommen wird",
                }
                ui.chip(
                    text="Kreditaufnahme",
                    icon="add",
                    color="indigo-3",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_increase = [
                    p for p in credit.increase if p.scenario == scenario
                ]
                for planPos in filtered_increase:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(planPos.value)}",
                            color="indigo-3",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": credit.increase,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt per wann eine Krediterhöhung erfolgt",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Betrag welcher zusätzlich als Kredit aufgenommen wird",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: credit.increase.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for change of the interest-rate
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_creditChips(card=card, credit=credit, scenario=scenario)

                params_new = {
                    "planPosList": credit.interestRate,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt ab wann neuer Zinssatz angewendet wird",
                    "valueLabel": "Zinssatz",
                    "valueFormat": "%.2f",
                    "valueProps": "suffix=%",
                }
                ui.chip(
                    text="Neuer Zinssatz",
                    icon="add",
                    color="orange",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_interestRate = [
                    p for p in credit.interestRate if p.scenario == scenario
                ]
                for planPos in filtered_interestRate:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(planPos.value,2)}%",
                            color="orange",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": credit.interestRate,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt ab wann neuer Zinssatz angewendet wird",
                                    "valueLabel": "Zinssatz",
                                    "valueFormat": "%.2f",
                                    "valueProps": "suffix=%",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: credit.interestRate.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)
