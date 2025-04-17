from nicegui import ui
from backend.classes.monthYear import MonthYear
from backend.classes.person import Person
from backend.tax.taxproperties import Taxation
from frontend.utils import *
from frontend.utils.confDialog import show_confDialog
from .personForm import show_personForm

expansionIsopen = False


def show_personOverview(person_card):
    person_card.clear()
    with person_card:

        # Header
        with ui.row().classes("justify-center items-center"):
            ui.label("Personen").classes("text-h6")

        # Table of entries
        with ui.column():
            rows = [
                {
                    "Name": r.name,
                    "Geburtsmonat": r.birth.dateToString(),
                }
                for r in Person.instanceDic.values()
            ]
            columns = [
                {"name": "Name", "label": "Name", "field": "Name", "align": "center"},
                {
                    "name": "Geburtsmonat",
                    "label": "Geburtsmonat",
                    "field": "Geburtsmonat",
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
                    on_click=lambda: show_personForm(person_card),
                ).props("flat unelevated")

                def edit_action():
                    if len(tbl.selected) != 1:
                        ui.notify("Wähle eine Zeile aus.")
                    else:
                        sel_name = tbl.selected[0]["Name"]
                        person = Person.get_itemByName(name=sel_name)
                        show_personForm(person_card, person=person)

                ui.button(icon="edit", on_click=edit_action).props("flat unelevated")

                async def del_action():
                    if len(tbl.selected) == 0:
                        ui.notify("Wähle mindestens eine Zeile aus.")
                    else:
                        if await show_confDialog():
                            for item in tbl.selected:
                                Person.get_itemByName(item["Name"]).delete_item()
                            ui.notify("Gelöscht", color="positive")
                            show_personOverview(person_card)  # simply refresh list

                ui.button(icon="delete", on_click=del_action).props("flat unelevated")
                ui.button(
                    icon="refresh",
                    on_click=lambda: show_personOverview(person_card),
                ).props("flat unelevated")
