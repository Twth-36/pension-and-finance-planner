import asyncio
from nicegui import ui

from backend.classes.cashflow import Cashflow
from backend.classes.expense import Expense
from backend.classes.income import Income
from backend.classes.pillar3bPolice import Pillar3bPolice
from frontend.utils.manageCashflow import dialog_Cashflow
from frontend.utils.manageExpense import dialog_Expense


def show_pillar3bPoliceDetail(
    card, pillar3bPolice: Pillar3bPolice = None, show_details: bool = False
):
    card.clear()
    with card:
        with ui.expansion(icon="tune", value=show_details) as detail_ext:

            # Expense-Position for deposits
            # needed functions
            def update_depositExpense(change):
                try:
                    pillar3bPolice.depositExpense = Expense.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_depositExpense():
                try:
                    if await dialog_Expense(pillar3bPolice.depositExpense):
                        show_pillar3bPoliceDetail(
                            card=card,
                            pillar3bPolice=pillar3bPolice,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_depositExpense():
                try:
                    new_expense = await dialog_Expense()
                    if new_expense:
                        pillar3bPolice.depositExpense = new_expense
                    show_pillar3bPoliceDetail(
                        card=card,
                        pillar3bPolice=pillar3bPolice,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):
                ui.select(
                    label="Einzahlungen",
                    options=[e.name for e in Expense.instanceDic.values()],
                    value=pillar3bPolice.depositExpense.name,
                    with_input=True,
                    on_change=update_depositExpense,
                ).tooltip(
                    "Ausgabeposition über welche die Säule 3b Einzahlungen verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_depositExpense,
                ).props(
                    "flat unelevated"
                ).tooltip("Ausgabeposition bearbeiten")

                ui.button(icon="add", on_click=new_depositExpense).props(
                    "flat unelevated"
                ).tooltip("Neue Ausgabeposition erstellen")

            # Cashflow-Position for payout
            # needed functions
            def update_payoutCF(change):
                try:
                    pillar3bPolice.payoutCF = Cashflow.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_payoutCF():
                try:
                    if await dialog_Cashflow(pillar3bPolice.payoutCF):
                        show_pillar3bPoliceDetail(
                            card=card,
                            pillar3bPolice=pillar3bPolice,
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
                        pillar3bPolice.payoutCF = new_CF
                    show_pillar3bPoliceDetail(
                        card=card,
                        pillar3bPolice=pillar3bPolice,
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
                    value=pillar3bPolice.payoutCF.name,
                    with_input=True,
                    on_change=update_payoutCF,
                ).tooltip(
                    "Cashflow-Position über welche die Auszahlung des Säule 3b-Gefässes verrechnet werden."
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

            # Income for pension
            # needed functions
            def update_pensionIncome(change):
                try:
                    pillar3bPolice.pensionIncome = Income.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_pensionIncome():
                try:
                    if await dialog_Cashflow(pillar3bPolice.payoutCF):
                        show_pillar3bPoliceDetail(
                            card=card,
                            pillar3bPolice=pillar3bPolice,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_pensionIncome():
                try:
                    new_Income = await dialog_Cashflow()
                    if new_Income:
                        pillar3bPolice.pensionIncome = new_Income
                    show_pillar3bPoliceDetail(
                        card=card,
                        pillar3bPolice=pillar3bPolice,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="Renteneinkommen",
                    options=[e.name for e in Income.instanceDic.values()],
                    value=pillar3bPolice.pensionIncome.name,
                    with_input=True,
                    on_change=update_pensionIncome,
                ).tooltip(
                    "Einkommensposition über welche die monatliche Rente des Säule 3b-Gefässes verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_pensionIncome,
                ).props(
                    "flat unelevated"
                ).tooltip("Einkommensposition bearbeiten")

                ui.button(icon="add", on_click=new_pensionIncome).props(
                    "flat unelevated"
                ).tooltip("Neue Einkommensposition erstellen")
