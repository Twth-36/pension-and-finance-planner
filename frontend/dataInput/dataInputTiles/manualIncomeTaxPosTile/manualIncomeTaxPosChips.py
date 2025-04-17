from nicegui import ui
from backend.classes.monthYear import MonthYear
from backend.classes.manualIncomeTaxPos import ManualIncomeTaxPos
from backend.classes.scenario import Scenario
from frontend.utils import *
from frontend.utils.format import formatswiss
from frontend.utils.managePlanPos import dialog_planPos


# chips:
def show_manualIncomeTaxPosChips(
    card, manualIncomeTaxPos: ManualIncomeTaxPos, scenario: Scenario
):
    card.clear()
    with card:
        with ui.row():
            # Chip for fixValue
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_manualIncomeTaxPosChips(
                            card=card,
                            manualIncomeTaxPos=manualIncomeTaxPos,
                            scenario=scenario,
                        )

                params_new = {
                    "planPosList": manualIncomeTaxPos.fixValue,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt per wann der neue Wert berücksichtigt werden soll. Relevant ist der Wert per Ende Dezember jedes Jahres",
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
                    r for r in manualIncomeTaxPos.fixValue if r.scenario == scenario
                ]
                for planPos in filtered_fixValues:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(value=planPos.value)}",
                            color="blue",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": manualIncomeTaxPos.fixValue,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt per wann der neue Wert berücksichtigt werden soll. Relevant ist der Wert per Ende Dezember jedes Jahres",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Betrag, welcher ab definierten Zeitpunkt berücksichtigt werden soll.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: manualIncomeTaxPos.fixValue.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)
