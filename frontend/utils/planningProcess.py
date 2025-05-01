import asyncio
from nicegui import ui

from backend.planning.mainPlanning import exe_mainPlanning
from backend.classes.scenario import Scenario


def show_planningProcess():
    with ui.dialog() as dialog, ui.card():
        ui.label("Wähle die zu berechnenden Szenarien aus")
        rows = [{"Name": item.name} for item in Scenario.instanceDic.values()]
        columns = [
            {
                "name": "Name",
                "label": "Name",
                "field": "Name",
                "align": "center",
            },
        ]
        tbl = ui.table(
            columns=columns, rows=rows, row_key="Name", selection="multiple"
        ).style("border: none; background-color: transparent;")
        tbl.selected = rows  # show all rows as selected

        checkbox_delObjects = ui.checkbox("Nicht benötigte Objekte löschen")

        async def start_planningProcess():
            dialog.clear()
            # use dialog as blocker during the calculations
            dialog.props('persistent backdrop-filter="blur(8px) brightness(40%)"')
            with dialog:
                ui.label("Dies dauert ein wenig...").classes("text-3xl text-white")
            n = ui.notification(
                message="Computing...", spinner=True, type="ongoing", timeout=None
            )

            # put exe_mainPlanning in queue
            await asyncio.to_thread(
                exe_mainPlanning,
                [Scenario.get_itemByName(item["Name"]) for item in tbl.selected],
                checkbox_delObjects.value,
            )
            ui.notify(
                "Geschafft! Denke daran deine aktuelle Seite allenfalls erneut zu laden.",
                color="positive",
            )

            n.dismiss()
            dialog.close()

        ui.button(icon="rocket", on_click=start_planningProcess).props(
            "flat unelevated"
        ).tooltip("Die Berechnung wird damit gestartet")
    dialog.open()
