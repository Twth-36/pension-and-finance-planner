from nicegui import ui
from backend.utils.monthYear import MonthYear
from backend.classes.person import Person
from backend.classes.realEstate import RealEstate
from backend.classes.scenario import Scenario
from frontend.dataInput.dataInputTiles.realEstateTile.realEstateDetails import (
    show_realEstateDetail,
)
from .realEstateChips import show_realEstateChips
from frontend.utils import *


def show_realEstateForm(realEstate_card, realEstate=None):
    realEstate_card.clear()
    with realEstate_card:
        with ui.row():
            with ui.column():
                # Input fields for data
                name_input = ui.input(
                    label="Name*",
                    value=(realEstate.name if realEstate else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")
                person_prefill = (
                    realEstate.person.name
                    if (realEstate and realEstate.person)
                    else None
                )
                person_input = ui.select(
                    label="Zugehörigkeit",
                    options=[p.name for p in Person.instanceDic.values()],
                    value=person_prefill,
                    with_input=True,
                )
                base_val_input = ui.number(
                    label="Wert",
                    value=(realEstate.baseValue if realEstate else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )
                taxValue_input = ui.number(
                    label="Steuerwert",
                    value=(realEstate.baseTaxValue if realEstate else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )
                taxRate_input = (
                    ui.number(
                        label="Steuersatz",
                        value=(realEstate.baseTaxValue if realEstate else None),
                        format="%.2f",
                    )
                    .props("suffix=%")
                    .tooltip("Steuersatz zur Berechnung der Liegenschaftssteuer.")
                )

                with ui.row():

                    def save_action():
                        try:
                            if realEstate:  # Update existing
                                if realEstate.name != name_input.value:
                                    realEstate.update_name(name_input.value)
                                realEstate.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if base_val_input.value:
                                    realEstate.baseValue = base_val_input.value
                                if taxValue_input.value:
                                    realEstate.baseTaxValue = taxValue_input.value
                                if taxRate_input.value:
                                    realEstate.taxRate = taxRate_input.value
                            else:  # Create new object
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if base_val_input.value:
                                    params["baseValue"] = base_val_input.value
                                if taxValue_input.value:
                                    params["baseTaxValue"] = taxValue_input.value
                                if taxRate_input.value:
                                    params["taxRate"] = taxRate_input.value
                                new_realEstate = RealEstate.create(**params)
                            # Refresh the form with updated object
                            if realEstate:
                                show_realEstateForm(realEstate_card, realEstate)
                            else:
                                show_realEstateForm(
                                    realEstate_card, realEstate=new_realEstate
                                )
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:\n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .realEstateOverview import show_realEstateOverview

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_realEstateOverview(realEstate_card),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_realEstateForm(
                            realEstate_card, realEstate
                        ),
                    ).props("flat unelevated")

            if realEstate and Scenario.instanceDic:

                with ui.column():

                    # Scenario-Selection for chips
                    scenario_select = ui.select(
                        label="Szenario",
                        options=[s.name for s in Scenario.instanceDic.values()],
                        value=next(s.name for s in Scenario.instanceDic.values()),
                        with_input=False,
                        on_change=lambda e: show_realEstateChips(
                            card=chip_card,  # ← this works because chip_card is defined in the same scope
                            realEstate=realEstate,
                            scenario=Scenario.get_itemByName(e.value),
                        ),
                    )

                    # Chip card comes below the select
                    chip_card = ui.column()

                    # Initial rendering of the chips
                    show_realEstateChips(
                        card=chip_card,
                        realEstate=realEstate,
                        scenario=Scenario.get_itemByName(scenario_select.value),
                    )

            # Detail-options
            if realEstate:
                detail_card = ui.column()
                show_realEstateDetail(card=detail_card, realEstate=realEstate)
