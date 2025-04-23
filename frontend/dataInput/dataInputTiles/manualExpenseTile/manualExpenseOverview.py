from nicegui import ui
from backend.utils.monthYear import MonthYear
from backend.classes.manualExpense import ManualExpense
from frontend.utils import *
from frontend.utils.confDialog import show_confDialog
from frontend.utils.format import formatswiss
from .manualExpenseForm import show_manualExpenseForm


def show_manualExpenseOverview(manualExpense_card):
    manualExpense_card.clear()
    with manualExpense_card:
        # Header
        with ui.row().classes("justify-center items-center"):
            ui.label("Ausgaben").classes("text-h6")
        # Table of entries
        with ui.column():
            rows = [
                {
                    "Name": r.name,
                    "Zugehörigkeit": (r.person.name if r.person else ""),
                    "Betrag": formatswiss(r.baseValue),
                }
                for r in ManualExpense.instanceDic.values()
            ]
            columns = [
                {"name": "Name", "label": "Name", "field": "Name", "align": "center"},
                {
                    "name": "Zugehörigkeit",
                    "label": "Zugehörigkeit",
                    "field": "Zugehörigkeit",
                    "align": "center",
                },
                {
                    "name": "Betrag",
                    "label": "Betrag",
                    "field": "Betrag",
                    "align": "center",
                },
            ]
            tbl = ui.table(
                columns=columns, rows=rows, row_key="Name", selection="multiple"
            ).style("border: none; background-color: transparent;")
            # Action buttons
            with ui.row().classes("items-center q-mb-sm"):
                ui.button(
                    icon="add",
                    on_click=lambda: show_manualExpenseForm(manualExpense_card),
                ).props("flat unelevated")

                def edit_action():
                    if len(tbl.selected) != 1:
                        ui.notify("Wähle eine Zeile aus.")
                    else:
                        sel_name = tbl.selected[0]["Name"]
                        manualExpense = ManualExpense.get_itemByName(name=sel_name)
                        show_manualExpenseForm(
                            manualExpense_card, manualExpense=manualExpense
                        )

                ui.button(icon="edit", on_click=edit_action).props("flat unelevated")

                async def del_action():
                    if len(tbl.selected) == 0:
                        ui.notify("Wähle mindestens eine Zeile aus.")
                    else:
                        if await show_confDialog():
                            for item in tbl.selected:
                                ManualExpense.get_itemByName(item["Name"]).delete_item()
                            ui.notify("Gelöscht", color="positive")
                            show_manualExpenseOverview(
                                manualExpense_card
                            )  # simply refresh list

                ui.button(icon="delete", on_click=del_action).props("flat unelevated")
                ui.button(
                    icon="refresh",
                    on_click=lambda: show_manualExpenseOverview(manualExpense_card),
                ).props("flat unelevated")
