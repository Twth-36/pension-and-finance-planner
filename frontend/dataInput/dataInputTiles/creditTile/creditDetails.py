import asyncio
from nicegui import ui

from backend.classes.cashflow import Cashflow
from backend.classes.expense import Expense
from backend.classes.credit import Credit
from frontend.utils.manageCashflow import dialog_Cashflow
from frontend.utils.manageExpense import dialog_Expense


def show_creditDetail(card, credit: Credit = None, show_details: bool = False):
    card.clear()
    with card:
        with ui.expansion(icon="tune", value=show_details) as detail_ext:

            # Expense-Position for interest-Rates
            # needed functions
            def update_interestExpense(change):
                try:
                    credit.interestExpense = Expense.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_interestExpense():
                try:
                    if await dialog_Expense(credit.interestExpense):
                        show_creditDetail(
                            card=card,
                            credit=credit,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_interestExpense():
                try:
                    new_expense = await dialog_Expense()
                    if new_expense:
                        credit.interestExpense = new_expense
                    show_creditDetail(
                        card=card,
                        credit=credit,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):
                ui.select(
                    label="Zinszahlungen",
                    options=[e.name for e in Expense.instanceDic.values()],
                    value=credit.interestExpense.name,
                    with_input=True,
                    on_change=update_interestExpense,
                ).tooltip(
                    "Ausgabeposition über welche die Zinszahlungen verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_interestExpense,
                ).props(
                    "flat unelevated"
                ).tooltip("Ausgabeposition bearbeiten")

                ui.button(icon="add", on_click=new_interestExpense).props(
                    "flat unelevated"
                ).tooltip("Neue Ausgabeposition erstellen")

            # Cashflow-Position for payback
            # needed functions
            def update_paybackCF(change):
                try:
                    credit.paybackCF = Cashflow.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_paybackCF():
                try:
                    if await dialog_Cashflow(credit.paybackCF):
                        show_creditDetail(
                            card=card,
                            credit=credit,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_paybackCF():
                try:
                    new_CF = await dialog_Cashflow()
                    if new_CF:
                        credit.paybackCF = new_CF
                    show_creditDetail(
                        card=card,
                        credit=credit,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="Amortisation",
                    options=[e.name for e in Cashflow.instanceDic.values()],
                    value=credit.paybackCF.name,
                    with_input=True,
                    on_change=update_paybackCF,
                ).tooltip(
                    "Cashflow-Position über welche eine Amortisation verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_paybackCF,
                ).props(
                    "flat unelevated"
                ).tooltip("Cashflow-Position bearbeiten")

                ui.button(icon="add", on_click=new_paybackCF).props(
                    "flat unelevated"
                ).tooltip("Neue Cashflow-Position erstellen")

            # Cashflow-Position for increase
            # needed functions
            def update_increaseCF(change):
                try:
                    credit.increaseCF = Cashflow.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_increaseCF():
                try:
                    if await dialog_Cashflow(credit.increaseCF):
                        show_creditDetail(
                            card=card,
                            credit=credit,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_increaseCF():
                try:
                    new_CF = await dialog_Cashflow()
                    if new_CF:
                        credit.increaseCF = new_CF
                    show_creditDetail(
                        card=card,
                        credit=credit,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="Kreditaufnahme",
                    options=[e.name for e in Cashflow.instanceDic.values()],
                    value=credit.increaseCF.name,
                    with_input=True,
                    on_change=update_increaseCF,
                ).tooltip(
                    "Cashflow-Position über welche eine Kreditaufnahme verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_increaseCF,
                ).props(
                    "flat unelevated"
                ).tooltip("Cashflow-Position bearbeiten")

                ui.button(icon="add", on_click=new_increaseCF).props(
                    "flat unelevated"
                ).tooltip("Neue Cashflow-Position erstellen")
