from nicegui import ui

from backend.classes.income import Income
from backend.classes.incomeTaxPos import IncomeTaxPos
from backend.classes.person import Person
from frontend.utils.manageIncomeTaxPos import dialog_IncomeTaxPos


def dialog_Income(income: Income = None):
    with ui.dialog() as dialog, ui.card():
        name_input = ui.input(
            label="Name*",
            value=income.name if income else None,
            validation={"Darf nicht leer sein": lambda v: len(v) > 0},
        ).props("autofocus")

        person_prefill = income.person.name if (income and income.person) else None
        person_input = ui.select(
            label="Zugehörigkeit",
            options=[p.name for p in Person.instanceDic.values()],
            value=person_prefill,
            with_input=True,
        )

        taxablePortion_input = (
            ui.number(
                label="Steuerbar",
                value=(income.taxablePortion if income else None),
                format="%.2f",
            )
            .props("suffix=%")
            .tooltip("Anteil, welcher als Einkommen versteuert werden muss.")
        )

        # income-Tax Position for Income

        with ui.row().classes("items-center gap-2"):
            incomeTaxPos_prefill = (
                income.taxPosition.name if (income and income.taxPosition) else None
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
                    if income:  # update existing
                        if income.name != name_input.value:
                            income.update_name(name_input.value)
                        income.person = (
                            Person.get_itemByName(person_input.value)
                            if person_input.value
                            else None
                        )

                        if taxablePortion_input.value:
                            income.taxablePortion = taxablePortion_input.value

                        if incomeTaxPos_input.value:
                            income.taxPosition = IncomeTaxPos.get_itemByName(
                                incomeTaxPos_input.value
                            )

                        dialog.submit(income)

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

                        new_Income = Income.create(**params)
                        dialog.submit(new_Income)

                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:\n{e}", color="negative")
                    dialog.submit(None)

            ui.button("Aktualisieren" if income else "Speichern", on_click=save_action)

            ui.button("Abbrechen", on_click=lambda: dialog.submit(None)).props(
                "outline"
            )

    return dialog
