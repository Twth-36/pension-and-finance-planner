from nicegui import ui
from backend.utils.monthYear import MonthYear
from backend.classes.person import Person
from backend.classes.manualExpense import ManualExpense
from backend.classes.scenario import Scenario
from frontend.dataInput.dataInputTiles.manualExpenseTile.manualExpenseDetails import (
    show_manualExpenseDetail,
)
from .manualExpenseChips import show_manualExpenseChips
from frontend.utils import *


def show_manualExpenseForm(manualExpense_card, manualExpense=None):
    manualExpense_card.clear()
    with manualExpense_card:
        with ui.row():
            with ui.column():
                # Input fields for data
                name_input = ui.input(
                    label="Name*",
                    value=(manualExpense.name if manualExpense else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")

                person_input = ui.select(
                    label="Zugehörigkeit",
                    options=[p.name for p in Person.instanceDic.values()],
                    value=(
                        manualExpense.person.name
                        if (manualExpense and manualExpense.person)
                        else None
                    ),
                    with_input=True,
                )
                with ui.row().classes("justify-center items-center"):
                    base_val_input = ui.number(
                        label="Betrag",
                        value=(manualExpense.baseValue if manualExpense else None),
                        validation={
                            "Muss grösser oder gleich 0 sein": lambda v: v is None
                            or v >= 0
                        },
                    )

                    MJ_toggle = ui.toggle({1: "M", 12: "J"}, value=1).tooltip(
                        "M: Monatswert, J: Jahreswert"
                    )

                inflationRate_input = ui.number(
                    label="Inflationsrate (p.a.)",
                    value=(
                        manualExpense.inflationRate
                        if (manualExpense and manualExpense.inflationRate is not None)
                        else 0
                    ),
                    format="%.1f",
                    suffix="%",
                ).tooltip("Definiert um wie viel sich die Ausgabe jährlich verteuert.")

                taxablePortion_input = ui.number(
                    label="Steuerlich Abzugsfähig",
                    value=(
                        manualExpense.taxablePortion
                        if (manualExpense and manualExpense.taxablePortion is not None)
                        else None
                    ),
                    format="%.0f",
                    suffix="%",
                    validation={
                        "Erwartet Wert zwischen 0 und 100": lambda v: (
                            v >= 0 and v <= 100
                        )
                    },
                ).tooltip(
                    "Definiert wie viel (in Prozent) dieser Ausgabe steuerlich abziehbar ist."
                )

                repetive_input = ui.checkbox(
                    text="Wiederholende Ausgabe",
                    value=(
                        manualExpense.repetitive if manualExpense is not None else True
                    ),
                ).tooltip(
                    "Falls es sich um eine einmalige Ausgabe handelt ist dieses Kästchen zu entfernen und die Planwerte über den Button 'Überschreibung Planungswert' zu pflegen."
                )

                with ui.row():

                    def save_action():
                        try:
                            if manualExpense:  # Update existing
                                if manualExpense.name != name_input.value:
                                    manualExpense.update_name(name_input.value)
                                manualExpense.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if base_val_input.value:
                                    manualExpense.baseValue = (
                                        base_val_input.value / MJ_toggle.value
                                    )
                                if inflationRate_input.value:
                                    manualExpense.inflationRate = (
                                        inflationRate_input.value
                                    )
                                if taxablePortion_input.value:
                                    manualExpense.taxablePortion = (
                                        taxablePortion_input.value
                                    )

                                manualExpense.repetitive = repetive_input.value
                            else:  # Create new object
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if base_val_input.value:
                                    params["baseValue"] = (
                                        base_val_input.value / MJ_toggle.value
                                    )
                                if inflationRate_input.value:
                                    params["inflationRate"] = inflationRate_input.value
                                if taxablePortion_input.value:
                                    params["taxablePortion"] = (
                                        taxablePortion_input.value
                                    )

                                params["repetitive"] = repetive_input.value
                                new_manualExpense = ManualExpense.create(**params)
                            # Refresh the form with updated object
                            if manualExpense:
                                show_manualExpenseForm(
                                    manualExpense_card, manualExpense
                                )
                            else:
                                show_manualExpenseForm(
                                    manualExpense_card, manualExpense=new_manualExpense
                                )
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:\n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .manualExpenseOverview import show_manualExpenseOverview

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_manualExpenseOverview(manualExpense_card),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_manualExpenseForm(
                            manualExpense_card, manualExpense
                        ),
                    ).props("flat unelevated")

            if manualExpense and Scenario.instanceDic:

                # vertical line for separation
                ui.separator().props("vertical")

                with ui.column():

                    # Scenario-Selection for chips
                    scenario_select = ui.select(
                        label="Szenario",
                        options=[s.name for s in Scenario.instanceDic.values()],
                        value=next(s.name for s in Scenario.instanceDic.values()),
                        with_input=False,
                        on_change=lambda e: show_manualExpenseChips(
                            card=chip_card,
                            manualExpense=manualExpense,
                            scenario=Scenario.get_itemByName(e.value),
                        ),
                    )

                    # Chip card comes below the select
                    chip_card = ui.column()

                    # Initial rendering of the chips
                    show_manualExpenseChips(
                        card=chip_card,
                        manualExpense=manualExpense,
                        scenario=Scenario.get_itemByName(scenario_select.value),
                    )

            if manualExpense:

                # vertical line for separation
                ui.separator().props("vertical")

                detail_card = ui.column()

                show_manualExpenseDetail(card=detail_card, manualExpense=manualExpense)
