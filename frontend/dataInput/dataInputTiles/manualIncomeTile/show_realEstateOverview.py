from nicegui import ui
from backend.classes.monthYear import MonthYear
from backend.classes.manualIncome import ManualIncome
from frontend.utils import *
from .show_manualIncomeForm import show_manualIncomeForm


def show_manualIncomeOverview(manualIncome_card):
    manualIncome_card.clear()
    with manualIncome_card:
        # Header
        with ui.row().classes("justify-center items-center"):
            ui.label("Liegenschaften").classes("text-h6")
        # Table of entries
        with ui.column():
            rows = [
                {
                    "Name": r.name,
                    "Zugehörigkeit": (r.person.name if r.person else ""),
                    "Betrag": formatswiss(r.baseValue),
                }
                for r in ManualIncome.instanceDic.values()
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
                    on_click=lambda: show_manualIncomeForm(manualIncome_card),
                ).props("flat unelevated")

                def edit_action():
                    if len(tbl.selected) != 1:
                        ui.notify("Wähle eine Zeile aus.")
                    else:
                        sel_name = tbl.selected[0]["Name"]
                        manualIncome = ManualIncome.get_itemByName(name=sel_name)
                        show_manualIncomeForm(
                            manualIncome_card, manualIncome=manualIncome
                        )

                ui.button(icon="edit", on_click=edit_action).props("flat unelevated")

                async def del_action():
                    if len(tbl.selected) == 0:
                        ui.notify("Wähle mindestens eine Zeile aus.")
                    else:
                        if await confDialog():
                            for item in tbl.selected:
                                ManualIncome.get_itemByName(item["Name"]).delete_item()
                            ui.notify("Gelöscht", color="positive")
                            show_manualIncomeOverview(
                                manualIncome_card
                            )  # simply refresh list

                ui.button(icon="delete", on_click=del_action).props("flat unelevated")
                ui.button(
                    icon="refresh",
                    on_click=lambda: show_manualIncomeOverview(manualIncome_card),
                ).props("flat unelevated")
