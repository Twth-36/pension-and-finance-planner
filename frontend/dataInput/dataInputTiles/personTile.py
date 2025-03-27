from nicegui import ui
from backend.classes.person import *
from backend.classes.monthYear import *
from backend.tax.taxproperties import *
from frontend.utils import *

# Global container that will hold either the table or the form.
main_container = ui.card().classes("q-pa-md")


def show_overview(showdetails=False):
    main_container.clear()
    with main_container:
        with ui.row().classes("justify-center items-center"):
            ui.label("Personen").classes("text-h6")
            detail_switch = ui.switch("Details:", value=showdetails).props("left-label")

        with ui.column().classes("q-mt-md"):

            # class variables:
            ## Taxation:
            def update_taxation(changes):
                try:
                    Person.taxation = Taxation(changes.value)
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht: \n {e}", color="negative")
                ui.notify("Änderung aktualisiert", color="positive")

            ui.select(
                label="Besteuerung",
                options=[member.value for member in Taxation],
                value=Person.taxation.value,
                on_change=update_taxation,  # sends automatically the changes as parameter
            ).tooltip(
                "Eine gemeinsame Besteuerung liegt bei verheiratetem Zivilstand vor."
                " Bei einzelner Besteuerung werden die Steuern jeder Person zum Alleinstehenden-Satz berechnet."
            ).bind_visibility_from(
                detail_switch, "value"
            )

            # Place:
            def update_place(new_place: str):
                try:
                    Person.place = new_place
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht: {e}", color="negative")
                ui.notify("Änderung aktualisiert", color="positive")

            place_input = (
                ui.input(
                    label="Wohnort",
                    value=Person.place if Person.place else "",
                )
                .tooltip("Wohnort für Besteuerung")
                .bind_visibility_from(detail_switch, "value")
            )

            place_input.on("blur", lambda: update_place(place_input.value))

            ## table with items:
            rows = []
            for item in Person.instanceDic.values():
                rows.append(
                    {
                        "Name": item.name,
                        "Geburtsmonat": item.birth.get_dateAsString(),
                    }
                )
            col_defs = [
                {"name": "Name", "label": "Name", "field": "Name", "align": "center"},
                {
                    "name": "Geburtsmonat",
                    "label": "Geburtsmonat",
                    "field": "Geburtsmonat",
                    "align": "center",
                },
            ]
            tbl = ui.table(
                columns=col_defs, rows=rows, row_key="Name", selection="multiple"
            ).style("border: none; background-color: transparent;")

            ## buttons for editing
            with ui.row().classes("items-center q-mb-sm"):
                ui.button(icon="add", on_click=show_person_form)

                def edit_action():
                    if len(tbl.selected) != 1:
                        ui.notify("Wähle eine Zeile aus.")
                    else:
                        show_person_form(
                            person=Person.get_itemByName(name=tbl.selected[0]["Name"])
                        )

                ui.button(icon="edit", on_click=edit_action)

                async def del_action():
                    if len(tbl.selected) == 0:
                        ui.notify("Wähle mindestens eine Zeile aus.")
                    else:
                        if await show_confDialog():
                            for item in tbl.selected:
                                Person.get_itemByName(item["Name"]).delete_item()

                            ui.notify("Gelöscht", color="positive")
                            show_overview(detail_switch.value)

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
        conf_input = ui.select(
            label="Konfession*",
            options=[member.value for member in Confession],
            value=person.conf.value if person else None,
            with_input=True,
        ).tooltip("Die Konfession wird für die korrekte Steuerberechnung verwendet.")

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
                        person.conf = Confession(conf_input.value)
                    else:
                        Person.create(
                            name=name_input.value,
                            birth=birth_input,
                            conf=Confession(conf_input.value),
                        )
                    show_overview()
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht: \n {e}", color="negative")

            btn_label = "Aktualisieren" if person else "Speichern"
            ui.button(btn_label, on_click=save_action)
            ui.button("Abbrechen", on_click=show_overview).props("outline")


def show_personTile():
    Person.create(
        name="tim", birth=MonthYear(month=11, year=1997), conf=Confession.ev_rev
    )
    Person.create(
        name="Lena", birth=MonthYear(month=10, year=1997), conf=Confession.roem_kath
    )
    show_overview()
