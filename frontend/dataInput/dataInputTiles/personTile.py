from nicegui import ui
from backend.classes.person import *
from backend.classes.monthYear import *
from backend.tax.taxproperties import *
from frontend.utils import *


def show_personTile():
    # Create a card container for the person tile
    person_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")

    # Nested function to display the overview table in this card
    def show_overview(showdetails=False):
        person_card.clear()
        with person_card:

            ui.label("Personen").classes("text-h6")
            with ui.expansion(icon="tune", value=showdetails) as detail_ext:
                # **Detail fields (Taxation and Place)**
                def update_taxation(change):
                    try:
                        Person.taxation = Taxation(change.value)
                    except Exception as e:
                        ui.notify(
                            f"Upps, etwas passte da nicht:\n{e}", color="negative"
                        )
                    ui.notify("Änderung aktualisiert", color="positive")

                ui.select(
                    label="Besteuerung",
                    options=[m.value for m in Taxation],
                    value=Person.taxation.value,
                    on_change=update_taxation,
                ).tooltip(
                    "Bei einzelner Besteuerung werden sämtliche Personen individuell zum Alleinstehenden-Satz besteuert."
                    "Positionen ohne Personenzuweisung werden je hälftig berücksichtigt. Andernfalls werden die Steuern kumuliert zum verheirateten-Satz berechnet."
                )

                def update_place(new_place: str):
                    try:
                        Person.place = new_place
                    except Exception as e:
                        ui.notify(f"Upps, etwas passte da nicht: {e}", color="negative")
                    ui.notify("Änderung aktualisiert", color="positive")

                place_input = (
                    ui.input(label="Wohnort", value=Person.place or "")
                    .tooltip("Wohnort für Besteuerung")
                    .bind_visibility_from(detail_ext, "value")
                )
                place_input.on("blur", lambda: update_place(place_input.value))

            # Content column (table and controls)
            with ui.column():
                # **Table of Person entries**
                rows = [
                    {"Name": p.name, "Geburtsmonat": p.birth.dateToString()}
                    for p in Person.instanceDic.values()
                ]
                columns = [
                    {
                        "name": "Name",
                        "label": "Name",
                        "field": "Name",
                        "align": "center",
                    },
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

                # **Action buttons (Add, Edit, Delete, Refresh)**
                with ui.row().classes("items-center q-mb-sm"):
                    ui.button(icon="add", on_click=lambda: show_person_form()).props(
                        "flat unelevated"
                    )

                    def edit_action():
                        if len(tbl.selected) != 1:
                            ui.notify("Wähle eine Zeile aus.")
                        else:
                            selected_name = tbl.selected[0]["Name"]
                            person = Person.get_itemByName(name=selected_name)
                            show_person_form(person=person)

                    ui.button(icon="edit", on_click=edit_action).props(
                        "flat unelevated"
                    )

                    async def del_action():
                        if len(tbl.selected) == 0:
                            ui.notify("Wähle mindestens eine Zeile aus.")
                        else:
                            if await confDialog():
                                for item in tbl.selected:
                                    Person.get_itemByName(item["Name"]).delete_item()
                                ui.notify("Gelöscht", color="positive")
                                # Refresh overview, preserving detail toggle state
                                show_overview(detail_ext.value)

                    ui.button(icon="delete", on_click=del_action).props(
                        "flat unelevated"
                    )

                    ui.button(
                        icon="refresh", on_click=lambda: show_overview(detail_ext.value)
                    ).props("flat unelevated")

        # Nested function to display the person form in this card
        def show_person_form(person=None):
            person_card.clear()
            with person_card:
                # Input fields for person data
                name_input = ui.input(
                    label="Name*",
                    value=(person.name if person else None),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")
                birth_input = ui.input(
                    label="Geburtsmonat*",
                    placeholder="MM.JJJJ",
                    validation={
                        "Format nicht korrekt": lambda v: MonthYear.validate_dateFormat(
                            v
                        )
                    },
                    value=person.birth.dateToString() if person else None,
                )
                conf_input = ui.select(
                    label="Konfession*",
                    options=[c.value for c in Confession],
                    value=(person.conf.value if person else None),
                    with_input=True,
                ).tooltip(
                    "Die Konfession wird für die korrekte Steuerberechnung verwendet."
                )

                # Form action buttons (Save/Update and Cancel)
                with ui.row():

                    def save_action():
                        try:

                            if person:  # Update existing person
                                if person.name != name_input.value:
                                    person.update_name(name_input.value)
                                person.birth = MonthYear.stringToDate(birth_input.value)
                                person.conf = Confession(conf_input.value)
                            else:  # Create new person
                                Person.create(
                                    name=name_input.value,
                                    birth=MonthYear.stringToDate(birth_input.value),
                                    conf=Confession(conf_input.value),
                                )
                            show_overview(
                                detail_ext.value
                            )  # Return to overview after saving
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht: {e}", color="negative"
                            )

                    btn_label = "Aktualisieren" if person else "Speichern"
                    ui.button(btn_label, on_click=save_action)
                    ui.button(
                        "Abbrechen", on_click=lambda: show_overview(detail_ext.value)
                    ).props("outline")

    show_overview()  # Display the overview in the card initially

    return person_card
