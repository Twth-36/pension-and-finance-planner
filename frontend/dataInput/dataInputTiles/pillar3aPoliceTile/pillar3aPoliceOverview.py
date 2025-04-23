from nicegui import ui
from backend.classes.pillar3aPolice import Pillar3aPolice, Person
from backend.utils.monthYear import MonthYear
from frontend.utils import *
from frontend.utils.confDialog import show_confDialog
from frontend.utils.format import formatswiss
from .pillar3aPoliceForm import show_pillar3aPoliceForm


def show_pillar3aPoliceOverview(pillar3aPolice_card):
    pillar3aPolice_card.clear()
    with pillar3aPolice_card:
        # Header
        with ui.row().classes("justify-center items-center"):
            ui.label("Säule 3a Policen").classes("text-h6")
        # Table of Pillar3aPolice entries
        with ui.column():
            rows = [
                {
                    "Name": c.name,
                    "Zugehörigkeit": (c.person.name if c.person else ""),
                    "Betrag": formatswiss(c.baseValue),
                }
                for c in Pillar3aPolice.instanceDic.values()
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
                    on_click=lambda: show_pillar3aPoliceForm(pillar3aPolice_card),
                ).props("flat unelevated")

                def edit_action():
                    if len(tbl.selected) != 1:
                        ui.notify("Wähle eine Zeile aus.")
                    else:
                        sel_name = tbl.selected[0]["Name"]
                        pillar3aPolice = Pillar3aPolice.get_itemByName(name=sel_name)
                        show_pillar3aPoliceForm(
                            pillar3aPolice_card, pillar3aPolice=pillar3aPolice
                        )

                ui.button(icon="edit", on_click=edit_action).props("flat unelevated")

                async def del_action():
                    if len(tbl.selected) == 0:
                        ui.notify("Wähle mindestens eine Zeile aus.")
                    else:
                        if await show_confDialog():
                            for item in tbl.selected:
                                Pillar3aPolice.get_itemByName(
                                    item["Name"]
                                ).delete_item()
                            ui.notify("Gelöscht", color="positive")
                            show_pillar3aPoliceOverview(
                                pillar3aPolice_card
                            )  # simply refresh list

                ui.button(icon="delete", on_click=del_action).props("flat unelevated")
                ui.button(
                    icon="refresh",
                    on_click=lambda: show_pillar3aPoliceOverview(pillar3aPolice_card),
                ).props("flat unelevated")
