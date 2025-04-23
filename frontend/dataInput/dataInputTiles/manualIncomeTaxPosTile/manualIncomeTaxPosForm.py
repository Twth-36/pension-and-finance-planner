from nicegui import ui
from backend.utils.monthYear import MonthYear
from backend.classes.person import Person
from backend.classes.manualIncomeTaxPos import ManualIncomeTaxPos
from backend.classes.scenario import Scenario
from backend.tax.taxproperties import TaxPositionType
from frontend.dataInput.dataInputTiles.manualIncomeTaxPosTile.manualIncomeTaxPosChips import *


from frontend.utils import *


def show_manualIncomeTaxPosForm(manualIncomeTaxPos_card, manualIncomeTaxPos=None):
    manualIncomeTaxPos_card.clear()
    with manualIncomeTaxPos_card:
        with ui.row():
            with ui.column():
                # Input fields for data
                name_input = ui.input(
                    label="Name*",
                    value=(manualIncomeTaxPos.name if manualIncomeTaxPos else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")

                person_input = ui.select(
                    label="Zugehörigkeit",
                    options=[p.name for p in Person.instanceDic.values()],
                    value=(
                        manualIncomeTaxPos.person.name
                        if (manualIncomeTaxPos and manualIncomeTaxPos.person)
                        else None
                    ),
                    with_input=True,
                )
                base_val_input = ui.number(
                    label="Betrag (pro Jahr)",
                    value=(
                        manualIncomeTaxPos.baseValue if manualIncomeTaxPos else None
                    ),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                ).tooltip(
                    "JAHRESBETRAG, welcher bei der Berechnung der Einkommenssteuer berücksichtigt werden soll."
                )

                type_input = ui.select(
                    label="Typ",
                    options=[m.value for m in TaxPositionType],
                    value=(
                        manualIncomeTaxPos.type.value
                        if manualIncomeTaxPos
                        else TaxPositionType.deduction.value
                    ),
                )

                with ui.row():

                    def save_action():
                        try:
                            if manualIncomeTaxPos:  # Update existing
                                if manualIncomeTaxPos.name != name_input.value:
                                    manualIncomeTaxPos.update_name(name_input.value)
                                manualIncomeTaxPos.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if base_val_input.value:
                                    manualIncomeTaxPos.baseValue = base_val_input.value

                                if type_input.value:
                                    manualIncomeTaxPos.type = TaxPositionType(
                                        type_input.value
                                    )

                            else:  # Create new object
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if base_val_input.value:
                                    params["baseValue"] = base_val_input.value

                                if type_input.value:
                                    params["type"] = TaxPositionType(type_input.value)

                                new_manualIncomeTaxPos = ManualIncomeTaxPos.create(
                                    **params
                                )
                            # Refresh the form with updated object
                            if manualIncomeTaxPos:
                                show_manualIncomeTaxPosForm(
                                    manualIncomeTaxPos_card, manualIncomeTaxPos
                                )
                            else:
                                show_manualIncomeTaxPosForm(
                                    manualIncomeTaxPos_card,
                                    manualIncomeTaxPos=new_manualIncomeTaxPos,
                                )
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:\n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .manualIncomeTaxPosOverview import (
                        show_manualIncomeTaxPosOverview,
                    )

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_manualIncomeTaxPosOverview(
                            manualIncomeTaxPos_card
                        ),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_manualIncomeTaxPosForm(
                            manualIncomeTaxPos_card, manualIncomeTaxPos
                        ),
                    ).props("flat unelevated")

            if manualIncomeTaxPos and Scenario.instanceDic:

                with ui.column():

                    # Scenario-Selection for chips
                    scenario_select = ui.select(
                        label="Szenario",
                        options=[s.name for s in Scenario.instanceDic.values()],
                        value=next(s.name for s in Scenario.instanceDic.values()),
                        with_input=False,
                        on_change=lambda e: show_manualIncomeTaxPosChips(
                            card=chip_card,  # ← this works because chip_card is defined in the same scope
                            manualIncomeTaxPos=manualIncomeTaxPos,
                            scenario=Scenario.get_itemByName(e.value),
                        ),
                    )

                    # Chip card comes below the select
                    chip_card = ui.column()

                    # Initial rendering of the chips
                    show_manualIncomeTaxPosChips(
                        card=chip_card,
                        manualIncomeTaxPos=manualIncomeTaxPos,
                        scenario=Scenario.get_itemByName(scenario_select.value),
                    )
