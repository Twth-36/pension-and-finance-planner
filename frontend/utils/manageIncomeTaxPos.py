from nicegui import ui

from backend.classes.incomeTaxPos import IncomeTaxPos
from backend.classes.person import Person


def dialog_IncomeTaxPos(incomeTaxPos: IncomeTaxPos = None):
    with ui.dialog() as dialog, ui.card():
        name_input = ui.input(
            label="Name*",
            value=incomeTaxPos.name if incomeTaxPos else None,
            validation={"Darf nicht leer sein": lambda v: len(v) > 0},
        ).props("autofocus")

        person_prefill = (
            incomeTaxPos.person.name if (incomeTaxPos and incomeTaxPos.person) else None
        )
        person_input = ui.select(
            label="Zugehörigkeit",
            options=[p.name for p in Person.instanceDic.values()],
            value=person_prefill,
            with_input=True,
        )

        with ui.row():

            def save_action():
                try:
                    if incomeTaxPos:  # update existing
                        if incomeTaxPos.name != name_input.value:
                            incomeTaxPos.update_name(name_input.value)
                        incomeTaxPos.person = (
                            Person.get_itemByName(person_input.value)
                            if person_input.value
                            else None
                        )

                        dialog.submit(incomeTaxPos)

                    else:  # create new object
                        params = {"name": name_input.value}
                        if person_input.value not in [None, ""]:
                            params["person"] = Person.get_itemByName(person_input.value)
                        else:
                            params["person"] = None

                        new_IncomeTaxPos = IncomeTaxPos.create(**params)
                        dialog.submit(new_IncomeTaxPos)

                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:\n{e}", color="negative")
                    dialog.submit(None)

            ui.button("Speichern", on_click=save_action)

            ui.button("Abbrechen", on_click=lambda: dialog.submit(None)).props(
                "outline"
            )

    return dialog
