import asyncio
from nicegui import ui

from backend.classes.cashflow import Cashflow
from backend.classes.expense import Expense
from backend.classes.realEstate import RealEstate
from frontend.utils.manageCashflow import dialog_Cashflow
from frontend.utils.manageExpense import dialog_Expense


def show_realEstateDetail(
    card, realEstate: RealEstate = None, show_details: bool = False
):
    card.clear()
    with card:
        with ui.expansion(icon="tune", value=show_details) as detail_ext:

            # Expense-Position for maintenanceCosts
            # needed functions
            def update_maintExpense(change):
                try:
                    realEstate.maintenanceExpense = Expense.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_MaintExpense():
                try:
                    if await dialog_Expense(realEstate.maintenanceExpense):
                        show_realEstateDetail(
                            card=card,
                            realEstate=realEstate,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_MaintExpense():
                try:
                    new_expense = await dialog_Expense()
                    if new_expense:
                        realEstate.maintenanceExpense = new_expense
                    show_realEstateDetail(
                        card=card,
                        realEstate=realEstate,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):
                ui.select(
                    label="Unterhaltskosten",
                    options=[e.name for e in Expense.instanceDic.values()],
                    value=realEstate.maintenanceExpense.name,
                    with_input=True,
                    on_change=update_maintExpense,
                ).tooltip(
                    "Ausgabeposition über welche die Unterhaltskosten verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_MaintExpense,
                ).props(
                    "flat unelevated"
                ).tooltip("Ausgabeposition bearbeiten")

                ui.button(icon="add", on_click=new_MaintExpense).props(
                    "flat unelevated"
                ).tooltip("Neue Ausgabeposition erstellen")

            # Expense-Position for realEstate-Taxes
            # needed functions
            def update_taxExpense(change):
                try:
                    realEstate.taxExpense = Expense.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_taxExpense():
                try:
                    if await dialog_Expense(realEstate.taxExpense):
                        show_realEstateDetail(
                            card=card,
                            realEstate=realEstate,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_taxExpense():
                try:
                    new_expense = await dialog_Expense()
                    if new_expense:
                        realEstate.taxExpense = new_expense
                    show_realEstateDetail(
                        card=card,
                        realEstate=realEstate,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="Liegenschaftssteuer",
                    options=[e.name for e in Expense.instanceDic.values()],
                    value=realEstate.taxExpense.name,
                    with_input=True,
                    on_change=update_taxExpense,
                ).tooltip(
                    "Ausgabeposition über welche die Liegenschaftssteuer verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_taxExpense,
                ).props(
                    "flat unelevated"
                ).tooltip("Ausgabeposition bearbeiten")

                ui.button(icon="add", on_click=new_taxExpense).props(
                    "flat unelevated"
                ).tooltip("Neue Ausgabeposition erstellen")

            # Expense-Position for renovations
            # needed functions
            def update_renovationExpense(change):
                try:
                    realEstate.renovationExpense = Expense.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_renovationExpense():
                try:
                    if await dialog_Expense(realEstate.renovationExpense):
                        show_realEstateDetail(
                            card=card,
                            realEstate=realEstate,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_taxExpense():
                try:
                    new_expense = await dialog_Expense()
                    if new_expense:
                        realEstate.renovationExpense = new_expense
                    show_realEstateDetail(
                        card=card,
                        realEstate=realEstate,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="Renovationen",
                    options=[e.name for e in Expense.instanceDic.values()],
                    value=realEstate.renovationExpense.name,
                    with_input=True,
                    on_change=update_renovationExpense,
                ).tooltip(
                    "Ausgabeposition über welche die Renovationen verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_renovationExpense,
                ).props(
                    "flat unelevated"
                ).tooltip("Ausgabeposition bearbeiten")

                ui.button(icon="add", on_click=new_taxExpense).props(
                    "flat unelevated"
                ).tooltip("Neue Ausgabeposition erstellen")

            # Cashflow-Position for purchase
            # needed functions
            def update_purchaseCF(change):
                try:
                    realEstate.purchaseCF = Cashflow.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_purchaseCF():
                try:
                    if await dialog_Cashflow(realEstate.purchaseCF):
                        show_realEstateDetail(
                            card=card,
                            realEstate=realEstate,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_purchaseCF():
                try:
                    new_CF = await dialog_Cashflow()
                    if new_CF:
                        realEstate.purchaseCF = new_CF
                    show_realEstateDetail(
                        card=card,
                        realEstate=realEstate,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="Kauf / Investitionen",
                    options=[e.name for e in Cashflow.instanceDic.values()],
                    value=realEstate.purchaseCF.name,
                    with_input=True,
                    on_change=update_purchaseCF,
                ).tooltip(
                    "Cashflow-Position über welche ein Kauf oder eine Investition verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_purchaseCF,
                ).props(
                    "flat unelevated"
                ).tooltip("Cashflow-Position bearbeiten")

                ui.button(icon="add", on_click=new_purchaseCF).props(
                    "flat unelevated"
                ).tooltip("Neue Cashflow-Position erstellen")

            # Cashflow-Position for sales
            # needed functions
            def update_saleCF(change):
                try:
                    realEstate.saleCF = Cashflow.get_itemByName(change.value)
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_saleCF():
                try:
                    if await dialog_Cashflow(realEstate.saleCF):
                        show_realEstateDetail(
                            card=card,
                            realEstate=realEstate,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_saleCF():
                try:
                    new_CF = await dialog_Cashflow()
                    if new_CF:
                        realEstate.saleCF = new_CF
                    show_realEstateDetail(
                        card=card,
                        realEstate=realEstate,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):

                ui.select(
                    label="Verkauf",
                    options=[e.name for e in Cashflow.instanceDic.values()],
                    value=realEstate.saleCF.name,
                    with_input=True,
                    on_change=update_saleCF,
                ).tooltip(
                    "Cashflow-Position über welche ein Verkauf verrechnet werden."
                )

                ui.button(
                    icon="edit",
                    on_click=edit_saleCF,
                ).props(
                    "flat unelevated"
                ).tooltip("Cashflow-Position bearbeiten")

                ui.button(icon="add", on_click=new_saleCF).props(
                    "flat unelevated"
                ).tooltip("Neue Cashflow-Position erstellen")
