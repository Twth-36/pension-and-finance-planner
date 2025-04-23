from nicegui import ui
from backend.utils.monthYear import MonthYear
from backend.classes.manualExpense import ManualExpense
from backend.classes.scenario import Scenario
from frontend.utils import *
from frontend.utils.format import formatswiss
from frontend.utils.managePlanPos import dialog_planPos


# chips:
def show_manualExpenseChips(card, manualExpense: ManualExpense, scenario: Scenario):
    card.clear()
    with card:
        with ui.row():
            # Chip for fixValue
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_manualExpenseChips(
                            card=card, manualExpense=manualExpense, scenario=scenario
                        )

                params_new = {
                    "planPosList": manualExpense.fixValue,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt per wann der neue monatliche Ausgabewert berücksichtigt werden soll.",
                    "valueLabel": "Betrag",
                    "valueTooltip": "Betrag, welcher ab definierten Zeitpunkt berücksichtigt werden soll.",
                }
                ui.chip(
                    text="Überschreibung Planungswert",
                    icon="add",
                    color="blue",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_fixValues = [
                    r for r in manualExpense.fixValue if r.scenario == scenario
                ]
                for planPos in filtered_fixValues:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(value=planPos.value)}",
                            color="blue",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": manualExpense.fixValue,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt per wann der neue monatliche Ausgabewert berücksichtigt werden soll.",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Betrag, welcher ab definierten Zeitpunkt berücksichtigt werden soll.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: manualExpense.fixValue.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)
