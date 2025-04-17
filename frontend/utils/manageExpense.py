from nicegui import ui

from backend.classes.expense import Expense
from backend.classes.incomeTaxPos import IncomeTaxPos
from backend.classes.person import Person
from frontend.utils.manageIncomeTaxPos import dialog_IncomeTaxPos


def dialog_Expense(expense: Expense = None):
    with ui.dialog() as dialog, ui.card():
        name_input = ui.input(
            label="Name*",
            value=expense.name if expense else None,
            validation={"Darf nicht leer sein": lambda v: len(v) > 0},
        ).props("autofocus")

        person_prefill = expense.person.name if (expense and expense.person) else None
        person_input = ui.select(
            label="Zugehörigkeit",
            options=[p.name for p in Person.instanceDic.values()],
            value=person_prefill,
            with_input=True,
        )

        taxablePortion_input = (
            ui.number(
                label="Steuerlich Abzugsfähig",
                value=(expense.taxablePortion if expense else None),
                format="%.2f",
            )
            .props("suffix=%")
            .tooltip(
                "Anteil, welcher als steuerlicher Abzug geltend gemacht werden darf."
            )
        )

        # income-Tax Position for Expense

        with ui.row().classes("items-center gap-2"):
            incomeTaxPos_prefill = (
                expense.taxPosition.name if (expense and expense.taxPosition) else None
            )

            incomeTaxPos_input = ui.select(
                label="Steuerposition",
                options=[e.name for e in IncomeTaxPos.instanceDic.values()],
                value=incomeTaxPos_prefill,
                with_input=True,
            ).tooltip(
                "Steuerposition, welche für die Berechnung der Einkommenssteuer verwendet wird."
            )

            async def edit_taxPos():
                try:
                    changed_taxPos = await dialog_IncomeTaxPos(
                        IncomeTaxPos.get_itemByName(incomeTaxPos_input.value)
                    )
                    if changed_taxPos:
                        incomeTaxPos_input.options = [
                            e.name for e in IncomeTaxPos.instanceDic.values()
                        ]
                        incomeTaxPos_input.value = changed_taxPos.name
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht: {e}",
                        color="negative",
                    )

            async def new_taxPos():
                try:
                    new_Pos = await dialog_IncomeTaxPos()
                    if new_Pos:
                        incomeTaxPos_input.clear()

                        incomeTaxPos_input.options = [
                            e.name for e in IncomeTaxPos.instanceDic.values()
                        ]
                        incomeTaxPos_input.value = new_Pos.name

                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht: {e}",
                        color="negative",
                    )

            ui.button(
                icon="edit",
                on_click=edit_taxPos,
            ).props(
                "flat unelevated"
            ).tooltip("Einkommenssteuer-Position bearbeiten")

            ui.button(icon="add", on_click=new_taxPos).props("flat unelevated").tooltip(
                "Neue Einkommenssteuer-Position erstellen"
            )

        with ui.row():

            def save_action():
                try:
                    if expense:  # update existing
                        if expense.name != name_input.value:
                            expense.update_name(name_input.value)
                        expense.person = (
                            Person.get_itemByName(person_input.value)
                            if person_input.value
                            else None
                        )

                        if taxablePortion_input.value:
                            expense.taxablePortion = taxablePortion_input.value

                        if incomeTaxPos_input.value:
                            expense.taxPosition = IncomeTaxPos.get_itemByName(
                                incomeTaxPos_input.value
                            )

                        dialog.submit(expense)

                    else:  # create new object
                        params = {"name": name_input.value}
                        if person_input.value not in [None, ""]:
                            params["person"] = Person.get_itemByName(person_input.value)
                        else:
                            params["person"] = None

                        if taxablePortion_input.value:
                            params["taxablePortion"] = taxablePortion_input.value

                        if incomeTaxPos_input.value:
                            params["taxPosition"] = IncomeTaxPos.get_itemByName(
                                incomeTaxPos_input.value
                            )

                        new_Expense = Expense.create(**params)
                        dialog.submit(new_Expense)

                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:\n{e}", color="negative")
                    dialog.submit(None)

            ui.button("Aktualisieren" if expense else "Speichern", on_click=save_action)

            ui.button("Abbrechen", on_click=lambda: dialog.submit(None)).props(
                "outline"
            )

    return dialog
