from nicegui import ui
from backend.classes.monthYear import MonthYear
from backend.classes.pensionFund import PensionFund
from backend.classes.scenario import Scenario
from frontend.dataInput.dataInputTiles.pensionFundTile.managePensFundPayoutPos import (
    dialog_pensFundPayoutPos,
)
from frontend.utils import *
from frontend.utils.format import formatswiss
from frontend.utils.managePlanPos import dialog_planPos


# chips:
def show_pensionFundChips(card, pensionFund: PensionFund, scenario: Scenario):
    card.clear()
    with card:
        with ui.row():
            # Chip for buyin
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_pensionFundChips(
                            card=card, pensionFund=pensionFund, scenario=scenario
                        )

                params_new = {
                    "planPosList": pensionFund.buyin,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt per wann der PK-Einkauf geplant ist. (Betrachte die steuerlichen Vorschriften für einen PK-Einkauf)",
                    "valueLabel": "Betrag",
                    "valueTooltip": "Betrag für PK-Einkauf (Beachte das ausgewiesene Einkaufspotential)",
                }
                ui.chip(
                    text="Einkauf",
                    icon="add",
                    color="blue",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_buyin = [
                    r for r in pensionFund.buyin if r.scenario == scenario
                ]
                for planPos in filtered_buyin:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(value=planPos.value)}",
                            color="blue",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": pensionFund.savingContribution,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt per wann der PK-Einkauf geplant ist. (Betrachte die steuerlichen Vorschriften für einen PK-Einkauf)",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Betrag für PK-Einkauf (Beachte das ausgewiesene Einkaufspotential)",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: pensionFund.buyin.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for savingcontribution
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_pensionFundChips(
                            card=card, pensionFund=pensionFund, scenario=scenario
                        )

                params_new = {
                    "planPosList": pensionFund.savingContribution,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt per der neue Sparbeitrag berücksichtigt werden soll.",
                    "valueLabel": "Sparbeitrag",
                    "valueTooltip": "Neuer Sparbeitrag welcher monatlich dem PK-Kapital gutgeschrieben wird.",
                }
                ui.chip(
                    text="Neuer Sparbeitrag",
                    icon="add",
                    color="indigo-3",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_savingContribution = [
                    r for r in pensionFund.savingContribution if r.scenario == scenario
                ]
                for planPos in filtered_savingContribution:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(value=planPos.value)}",
                            color="indigo-3",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": pensionFund.savingContribution,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt per der neue Sparbeitrag berücksichtigt werden soll.",
                                    "valueLabel": "Sparbeitrag",
                                    "valueTooltip": "Neuer Sparbeitrag welcher monatlich dem PK-Kapital gutgeschrieben wird.",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: pensionFund.buyin.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for fixValue
            with ui.column():

                async def edit_planPos(params):
                    if await dialog_planPos(**params):
                        show_pensionFundChips(
                            card=card, pensionFund=pensionFund, scenario=scenario
                        )

                params_new = {
                    "planPosList": pensionFund.fixValue,
                    "scenario": scenario,
                    "periodLabel": "Monat",
                    "periodTooltip": "Zeitpunkt per wann der Planungswert der PK überschrieben werd.",
                    "valueLabel": "Betrag",
                    "valueTooltip": "Voraussichtliches Alterskapital zum entsprechenden Zeitpunkt",
                }
                ui.chip(
                    text="Überschreibung Planungswert",
                    icon="add",
                    color="orange",
                    removable=False,
                    on_click=lambda param=params_new: edit_planPos(param),
                )

                filtered_fixValues = [
                    r for r in pensionFund.fixValue if r.scenario == scenario
                ]
                for planPos in filtered_fixValues:

                    def create_chip(planPos):
                        ui.chip(
                            text=f"{planPos.period.dateToString()}: {formatswiss(value=planPos.value)}",
                            color="orange",
                            removable=True,
                            on_click=lambda p=planPos: edit_planPos(
                                {
                                    "planPosList": pensionFund.fixValue,
                                    "planPos": p,
                                    "periodLabel": "Monat",
                                    "periodTooltip": "Zeitpunkt per wann der Planungswert der PK überschrieben werd.",
                                    "valueLabel": "Betrag",
                                    "valueTooltip": "Voraussichtliches Alterskapital zum entsprechenden Zeitpunkt",
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=planPos: pensionFund.fixValue.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(planPos)

            # Chip for payout
            with ui.column():

                async def edit_payoutPos(params):
                    if await dialog_pensFundPayoutPos(**params):
                        show_pensionFundChips(
                            card=card, pensionFund=pensionFund, scenario=scenario
                        )

                params_new = {
                    "payoutPosList": pensionFund.payout,
                    "scenario": scenario,
                }
                ui.chip(
                    text="(Teil-)Pensionierung",
                    icon="add",
                    color="grey",
                    removable=False,
                    on_click=lambda param=params_new: edit_payoutPos(param),
                )

                filtered_payout = [
                    r for r in pensionFund.payout if r.scenario == scenario
                ]
                for payoutPos in filtered_payout:

                    def create_chip(payoutPos):
                        ui.chip(
                            text=f"{payoutPos.period.dateToString()}: {formatswiss(value=payoutPos.value)}",
                            color="grey",
                            removable=True,
                            on_click=lambda p=payoutPos: edit_payoutPos(
                                {
                                    "payoutPosList": pensionFund.payout,
                                    "payoutPos": p,
                                }
                            ),
                        ).on(
                            "remove",
                            lambda p=payoutPos: pensionFund.payout.remove(p),
                        ).props(
                            "outline"
                        )

                    create_chip(payoutPos)
