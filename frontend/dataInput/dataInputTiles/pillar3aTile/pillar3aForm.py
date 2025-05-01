from nicegui import ui
from backend.classes.pillar3a import Pillar3a, Person
from backend.utils.monthYear import MonthYear
from backend.classes.realEstate import *
from frontend.dataInput.dataInputTiles.pillar3aTile.pillar3aDetails import (
    show_pillar3aDetail,
)

from .pillar3aChips import show_pillar3aChips
from frontend.utils import *


def show_pillar3aForm(pillar3a_card, pillar3a=None):
    pillar3a_card.clear()
    with pillar3a_card:
        with ui.row():
            with ui.column():
                # Input fields for pillar3a data
                name_input = ui.input(
                    label="Name*",
                    value=(pillar3a.name if pillar3a else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")

                person_prefill = (
                    pillar3a.person.name if (pillar3a and pillar3a.person) else None
                )
                person_input = ui.select(
                    label="Zugehörigkeit",
                    options=[p.name for p in Person.instanceDic.values()],
                    value=person_prefill,
                    with_input=True,
                )
                baseValue_input = ui.number(
                    label="Wert",
                    value=(pillar3a.baseValue if pillar3a else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )
                returnRate_input = ui.number(
                    label="Erwartete Rendite",
                    value=(pillar3a.returnRate if pillar3a else None),
                    format="%.2f",
                ).props("suffix=%")

                with ui.row():

                    def save_action():
                        try:
                            if pillar3a:  # Update existing
                                if pillar3a.name != name_input.value:
                                    pillar3a.update_name(name_input.value)
                                pillar3a.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if baseValue_input.value:
                                    pillar3a.baseValue = baseValue_input.value
                                if returnRate_input.value:
                                    pillar3a.returnRate = returnRate_input.value

                            else:  # Create new pillar3a
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if baseValue_input.value:
                                    params["baseValue"] = baseValue_input.value
                                if returnRate_input.value:
                                    params["returnRate"] = returnRate_input.value

                                new_pillar3a = Pillar3a.create(**params)
                            # Refresh the form with updated pillar3a
                            if pillar3a:
                                show_pillar3aForm(pillar3a_card, pillar3a)
                            else:
                                show_pillar3aForm(pillar3a_card, pillar3a=new_pillar3a)
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:  \n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .pillar3aOverview import show_pillar3aOverview

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_pillar3aOverview(pillar3a_card),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_pillar3aForm(pillar3a_card, pillar3a),
                    ).props("flat unelevated")

            if pillar3a and Scenario.instanceDic:

                # vertical line for separation
                ui.separator().props("vertical")

                with ui.column():

                    # Scenario-Selection for chips
                    scenario_select = ui.select(
                        label="Szenario",
                        options=[s.name for s in Scenario.instanceDic.values()],
                        value=next(s.name for s in Scenario.instanceDic.values()),
                        with_input=False,
                        on_change=lambda e: show_pillar3aChips(
                            card=chip_card,  # ← this works because chip_card is defined in the same scope
                            pillar3a=pillar3a,
                            scenario=Scenario.get_itemByName(e.value),
                        ),
                    )

                    # Chip card comes below the select
                    chip_card = ui.column()

                    # Initial rendering of the chips
                    show_pillar3aChips(
                        card=chip_card,
                        pillar3a=pillar3a,
                        scenario=Scenario.get_itemByName(scenario_select.value),
                    )

            # Detail-options
            if pillar3a:

                # vertical line for separation
                ui.separator().props("vertical")

                detail_card = ui.column()
                show_pillar3aDetail(card=detail_card, pillar3a=pillar3a)
