from nicegui import ui
from backend.utils.monthYear import MonthYear
from backend.classes.person import Person
from backend.classes.person import Person
from backend.tax.taxproperties import Confession
from frontend.utils import *


def show_personForm(person_card, person=None):
    person_card.clear()
    with person_card:
        with ui.row():
            with ui.column():
                # Input fields for data
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
                            show_personOverview(
                                person_card
                            )  # Return to overview after saving
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:  \n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .personOverview import show_personOverview

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_personOverview(person_card),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_personForm(person_card, person),
                    ).props("flat unelevated")
