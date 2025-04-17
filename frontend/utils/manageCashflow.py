from nicegui import ui

from backend.classes.cashflow import Cashflow
from backend.classes.person import Person


def dialog_Cashflow(cashflow: Cashflow = None):
    with ui.dialog() as dialog, ui.card():
        name_input = ui.input(
            label="Name*",
            value=cashflow.name if cashflow else None,
            validation={"Darf nicht leer sein": lambda v: len(v) > 0},
        ).props("autofocus")

        person_prefill = (
            cashflow.person.name if (cashflow and cashflow.person) else None
        )
        person_input = ui.select(
            label="Zugehörigkeit",
            options=[p.name for p in Person.instanceDic.values()],
            value=person_prefill,
            with_input=True,
        )

        taxablePortion_input = (
            ui.number(
                label="Kapitalauszahlungssteuer unterliegend",
                value=(cashflow.taxablePortion if cashflow else None),
                format="%.2f",
            )
            .props("suffix=%")
            .tooltip("Anteil, welcher der Kapitalauszahlungssteuer unterliegt")
        )

        with ui.row():

            def save_action():
                try:
                    if cashflow:  # update existing
                        if cashflow.name != name_input.value:
                            cashflow.update_name(name_input.value)
                        cashflow.person = (
                            Person.get_itemByName(person_input.value)
                            if person_input.value
                            else None
                        )

                        if taxablePortion_input.value:
                            cashflow.taxablePortion = taxablePortion_input.value

                        dialog.submit(cashflow)

                    else:  # create new object
                        params = {"name": name_input.value}
                        if person_input.value not in [None, ""]:
                            params["person"] = Person.get_itemByName(person_input.value)
                        else:
                            params["person"] = None

                        if taxablePortion_input.value:
                            params["taxablePortion"] = taxablePortion_input.value

                        new_Cashflow = Cashflow.create(**params)
                        dialog.submit(new_Cashflow)

                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:\n{e}", color="negative")
                    dialog.submit(None)

            ui.button(
                "Aktualisieren" if cashflow else "Speichern", on_click=save_action
            )

            ui.button("Abbrechen", on_click=lambda: dialog.submit(None)).props(
                "outline"
            )

    return dialog
