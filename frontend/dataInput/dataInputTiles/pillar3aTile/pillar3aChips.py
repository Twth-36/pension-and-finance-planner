from nicegui import ui
from backend.classes.pillar3a import Pillar3a, Person
from backend.utils.monthYear import MonthYear
from backend.classes.scenario import Scenario
from frontend.utils.format import formatswiss
from frontend.utils.managePlanPos import dialog_planPos


# chips:
def show_pillar3aChips(card, pillar3a: Pillar3a, scenario: Scenario):
    card.clear()
    with card:
        with ui.row():
            # Chip for deposits
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_pillar3aChips(
                            card=card, pillar3a=pillar3a, scenario=scenario
                        )

                params_new = {
                    "planPosList": pillar3a.deposit,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt der Einzahlung",
                    "valueLabel": "Betrag",
                    "valueTooltip": "Betrag, welches in das Säule3a-Gefäss einbezahlt wird.",
                }
                ui.chip(
                    text="Einzahlung",
                    icon="add",
                    color="blue",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_deposit = [
                    p for p in pillar3a.deposit if p.scenario == scenario
                ]
                for planPos in filtered_deposit:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(value=planPos.value)}",
                            color="blue",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": pillar3a.deposit,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt der Einzahlung",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Betrag, welches in das Säule3a-Gefäss einbezahlt wird.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: pillar3a.deposit.remove(p),
                        ).props(
                            "outline"
                        ).tooltip(
                            "Sofern nicht gepflegt erfolgt die Einzahlung in das steuerlich am besten geeignete Säule 3a-Gefäss."
                        )

                    create_chip(planPos)

            # Chip for payoutDate of the pillar3a
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_pillar3aChips(
                            card=card, pillar3a=pillar3a, scenario=scenario
                        )

                params_new = {
                    "planPosList": pillar3a.payoutDate,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt der Auszahlung des Säule3a-Gefässes",
                    "showValue": False,
                }
                ui.chip(
                    text="Bezug",
                    icon="add",
                    color="indigo-3",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                ).tooltip(
                    "Sofern nicht gepflegt wird der steuerlich beste Bezugszeitpunkt verwendet."
                )

                filtered_payoutDate = [
                    p for p in pillar3a.payoutDate if p.scenario == scenario
                ]
                for planPos in filtered_payoutDate:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}",
                            color="indigo-3",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": pillar3a.payoutDate,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt der Auszahlung des Säule3a-Gefässes",
                                    "showValue": False,
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: pillar3a.payoutDate.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)
