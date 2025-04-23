import asyncio
from nicegui import ui

from backend.classes.cashflow import Cashflow
from backend.classes.expense import Expense
from backend.classes.vestedBenefit import VestedBenefit
from frontend.utils.manageCashflow import dialog_Cashflow
from frontend.utils.manageExpense import dialog_Expense


def show_vestedBenefitDetail(
    card, vestedBenefit: VestedBenefit = None, show_details: bool = False
):
    card.clear()
    with card:
        with ui.expansion(icon="tune", value=show_details) as detail_ext:

            # Cashflow-Position for payout
            # needed functions
            def update_payoutCF(change):
                try:
                    vestedBenefit.payoutCF = Cashflow.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_payoutCF():
                try:
                    if await dialog_Cashflow(vestedBenefit.payoutCF):
                        show_vestedBenefitDetail(
                            card=card,
                            vestedBenefit=vestedBenefit,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_payoutCF():
                try:
                    new_CF = await dialog_Cashflow()
                    if new_CF:
                        vestedBenefit.payoutCF = new_CF
                    show_vestedBenefitDetail(
                        card=card,
                        vestedBenefit=vestedBenefit,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="Auszahlung",
                    options=[e.name for e in Cashflow.instanceDic.values()],
                    value=vestedBenefit.payoutCF.name,
                    with_input=True,
                    on_change=update_payoutCF,
                ).tooltip(
                    "Cashflow-Position über welche die Auszahlung des Säule 3a-Gefässes verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_payoutCF,
                ).props(
                    "flat unelevated"
                ).tooltip("Cashflow-Position bearbeiten")

                ui.button(icon="add", on_click=new_payoutCF).props(
                    "flat unelevated"
                ).tooltip("Neue Cashflow-Position erstellen")
