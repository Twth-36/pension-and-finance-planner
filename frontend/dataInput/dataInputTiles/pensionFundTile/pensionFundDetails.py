import asyncio
from nicegui import ui

from backend.classes.cashflow import Cashflow
from backend.classes.expense import Expense
from backend.classes.income import Income
from backend.classes.pensionFund import PensionFund
from frontend.utils.manageCashflow import dialog_Cashflow
from frontend.utils.manageExpense import dialog_Expense
from frontend.utils.manageIncome import dialog_Income


def show_pensionFundDetail(
    card, pensionFund: PensionFund = None, show_details: bool = False
):
    card.clear()
    with card:
        with ui.expansion(icon="tune", value=show_details) as detail_ext:

            # Expense-Position for buyin
            # needed functions
            def update_buyInExpense(change):
                try:
                    pensionFund.buyinExpense = Expense.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_buyInExpense():
                try:
                    if await dialog_Expense(pensionFund.buyinExpense):
                        show_pensionFundDetail(
                            card=card,
                            pensionFund=pensionFund,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_buyInExpense():
                try:
                    new_expense = await dialog_Expense()
                    if new_expense:
                        pensionFund.buyinExpense = new_expense
                    show_pensionFundDetail(
                        card=card,
                        pensionFund=pensionFund,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):
                ui.select(
                    label="Pensionskasseneinkauf",
                    options=[e.name for e in Expense.instanceDic.values()],
                    value=pensionFund.buyinExpense.name,
                    with_input=True,
                    on_change=update_buyInExpense,
                ).tooltip(
                    "Ausgabeposition über welche die Pensionskasseneinkäufe verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_buyInExpense,
                ).props(
                    "flat unelevated"
                ).tooltip("Ausgabeposition bearbeiten")

                ui.button(icon="add", on_click=new_buyInExpense).props(
                    "flat unelevated"
                ).tooltip("Neue Ausgabeposition erstellen")

            # Cashflow-Position for payout
            # needed functions
            def update_pensionCF(change):
                try:
                    pensionFund.pensionCF = Cashflow.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_pensionCF():
                try:
                    if await dialog_Cashflow(pensionFund.pensionCF):
                        show_pensionFundDetail(
                            card=card,
                            pensionFund=pensionFund,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_pensionCF():
                try:
                    new_CF = await dialog_Cashflow()
                    if new_CF:
                        pensionFund.pensionCF = new_CF
                    show_pensionFundDetail(
                        card=card,
                        pensionFund=pensionFund,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="Kapitalauszahlung",
                    options=[e.name for e in Cashflow.instanceDic.values()],
                    value=pensionFund.pensionCF.name,
                    with_input=True,
                    on_change=update_pensionCF,
                ).tooltip(
                    "Cashflow-Position über welche eine Kapitalauszahlung verrechnet wird."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_pensionCF,
                ).props(
                    "flat unelevated"
                ).tooltip("Cashflow-Position bearbeiten")

                ui.button(icon="add", on_click=new_pensionCF).props(
                    "flat unelevated"
                ).tooltip("Neue Cashflow-Position erstellen")

            # Cashflow-Position for payout
            # needed functions
            def update_pensionIncome(change):
                try:
                    pensionFund.pensionIncome = Income.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_pensionIncome():
                try:
                    if await dialog_Income(pensionFund.pensionIncome):
                        show_pensionFundDetail(
                            card=card,
                            pensionFund=pensionFund,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_pensionIncome():
                try:
                    new_income = await dialog_Income()
                    if new_income:
                        pensionFund.pensionIncome = new_income
                    show_pensionFundDetail(
                        card=card,
                        pensionFund=pensionFund,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="PK-Rente",
                    options=[e.name for e in Income.instanceDic.values()],
                    value=pensionFund.pensionIncome.name,
                    with_input=True,
                    on_change=update_pensionIncome,
                ).tooltip(
                    "Einkommensposition über welche eine PK-Rente verrechnet wird."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_pensionIncome,
                ).props(
                    "flat unelevated"
                ).tooltip("Einkommensposition bearbeiten")

                ui.button(icon="add", on_click=new_pensionCF).props(
                    "flat unelevated"
                ).tooltip("Neue Einkommensposition erstellen")
