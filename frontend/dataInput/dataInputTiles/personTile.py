from nicegui import ui
from backend.classes.person import Person
from backend.classes.monthYear import *
from frontend.utils import *

# Global container that will hold either the table or the form.
main_container = ui.card().classes("q-pa-md")


def show_overview():
    main_container.clear()
    with main_container:

        # Build table from instanceDic
        ui.label("Personen").classes("text-h6")
        with ui.column().classes("q-mt-md"):
            rows = []
            for person in Person.instanceDic.values():
                rows.append(
                    {
                        "Name": person.name,
                        "Geburtsmonat": person.birth.get_dateAsString(),
                    }
                )
            col_defs = [
                {"name": "Name", "label": "Name", "field": "Name"},
                {
                    "name": "Geburtsmonat",
                    "label": "Geburtsmonat",
                    "field": "Geburtsmonat",
                },
            ]
            tbl = ui.table(
                columns=col_defs, rows=rows, row_key="Name", selection="multiple"
            ).style("border: none; background-color: transparent;")

            with ui.row().classes("items-center q-mb-sm"):
                ui.button(icon="add", on_click=show_person_form)

                def edit_action():
                    print(tbl.selected)
                    if len(tbl.selected) != 1:
                        ui.notify("Wähle eine Zeile aus.", color="negative")
                    else:
                        show_person_form(
                            person=Person.get_itemByName(name=tbl.selected[0]["Name"])
                        )

                ui.button(icon="edit", on_click=edit_action)

                async def del_action():
                    if await show_confDialog():
                        ui.notify("Gelöscht")

                ui.button(icon="delete", on_click=del_action)


def show_person_form(person=None):
    main_container.clear()
    with main_container:

        name_input = ui.input(
            label="Name*",
            value=person.name if person else "",
            validation={"Darf nicht leer sein": lambda value: len(value) > 0},
        ).props("autofocus")
        month_input = ui.select(
            label="Geburtsmonat*",
            options=list(range(1, 13)),
            value=person.birth.month if person else None,
            with_input=True,
        )
        year_input = ui.select(
            label="Geburtsjahr*",
            options=list(range(get_currentDate().year - 100, get_currentDate().year)),
            value=person.birth.year if person else None,
            with_input=True,
        )

        with ui.row().classes("q-mt-md"):

            def save_action():
                try:
                    birth_input = MonthYear(
                        month=int(month_input.value), year=int(year_input.value)
                    )
                    if person:
                        if person.name != name_input.value:
                            person.update_name(name_input.value)
                        person.birth = birth_input
                    else:
                        Person.create(name=name_input.value, birth=birth_input)
                    show_overview()
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht: \n {e}", color="negative")

            btn_label = "Aktualisieren" if person else "Speichern"
            ui.button(btn_label, on_click=save_action)
            ui.button("Abbrechen", on_click=show_overview).props("outline")


def show_personTile():
    Person.create(name="tim", birth=MonthYear(month=11, year=1997))
    Person.create(name="Lena", birth=MonthYear(month=10, year=1997))
    show_overview()
