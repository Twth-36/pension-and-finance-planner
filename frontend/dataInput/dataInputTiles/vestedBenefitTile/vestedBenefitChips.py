from nicegui import ui
from backend.classes.vestedBenefit import VestedBenefit, Person
from backend.utils.monthYear import MonthYear
from backend.classes.scenario import Scenario
from frontend.utils.format import formatswiss
from frontend.utils.managePlanPos import dialog_planPos


# chips:
def show_vestedBenefitChips(card, vestedBenefit: VestedBenefit, scenario: Scenario):
    card.clear()
    with card:
        with ui.row():

            # Chip for payoutDate of the vestedBenefit
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_vestedBenefitChips(
                            card=card, vestedBenefit=vestedBenefit, scenario=scenario
                        )

                params_new = {
                    "planPosList": vestedBenefit.payoutDate,
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
                    p for p in vestedBenefit.payoutDate if p.scenario == scenario
                ]
                for planPos in filtered_payoutDate:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}",
                            color="indigo-3",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": vestedBenefit.payoutDate,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt der Auszahlung des Säule3a-Gefässes",
                                    "showValue": False,
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: vestedBenefit.payoutDate.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)
