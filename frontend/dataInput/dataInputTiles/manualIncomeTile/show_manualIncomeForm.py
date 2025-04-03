from nicegui import ui
from backend.classes.monthYear import MonthYear
from backend.classes.person import Person
from backend.classes.manualIncome import ManualIncome
from .show_manualIncomeChips import show_manualIncomeChips
from frontend.utils import *


def show_manualIncomeForm(manualIncome_card, manualIncome=None):
    manualIncome_card.clear()
    with manualIncome_card:
        with ui.row():
            with ui.column():
                # Input fields for data
                name_input = ui.input(
                    label="Name*",
                    value=(manualIncome.name if manualIncome else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")
                person_prefill = (
                    manualIncome.person.name
                    if (manualIncome and manualIncome.person)
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
                    value=(manualIncome.baseValue if manualIncome else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )
                taxValue_input = ui.number(
                    label="Steuerwert",
                    value=(manualIncome.baseTaxValue if manualIncome else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )
                taxRate_input = (
                    ui.number(
                        label="Steuersatz",
                        value=(manualIncome.baseTaxValue if manualIncome else None),
                        format="%.2f",
                    )
                    .props("suffix=%")
                    .tooltip("Steuersatz zur Berechnung der Liegenschaftssteuer.")
                )

                with ui.row():

                    def save_action():
                        try:
                            if manualIncome:  # Update existing
                                if manualIncome.name != name_input.value:
                                    manualIncome.update_name(name_input.value)
                                manualIncome.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if base_val_input.value:
                                    manualIncome.baseValue = base_val_input.value
                                if taxValue_input.value:
                                    manualIncome.baseTaxValue = taxValue_input.value
                                if taxRate_input.value:
                                    manualIncome.taxRate = taxRate_input.value
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
                                new_manualIncome = ManualIncome.create(**params)
                            # Refresh the form with updated object
                            if manualIncome:
                                show_manualIncomeForm(manualIncome_card, manualIncome)
                            else:
                                show_manualIncomeForm(
                                    manualIncome_card, manualIncome=new_manualIncome
                                )
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:\n{e}", color="negative"
                            )

                    btn_label = "Aktualisieren" if manualIncome else "Speichern"
                    ui.button(btn_label, on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .show_manualIncomeOverview import show_manualIncomeOverview

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_manualIncomeOverview(manualIncome_card),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_manualIncomeForm(
                            manualIncome_card, manualIncome
                        ),
                    ).props("flat unelevated")

            if manualIncome and Scenario.instanceDic:

                with ui.column():

                    # Scenario-Selection for chips
                    scenario_select = ui.select(
                        label="Szenario",
                        options=[s.name for s in Scenario.instanceDic.values()],
                        value=next(s.name for s in Scenario.instanceDic.values()),
                        with_input=False,
                        on_change=lambda e: show_manualIncomeChips(
                            card=chip_card,  # ← this works because chip_card is defined in the same scope
                            manualIncome=manualIncome,
                            scenario=Scenario.get_itemByName(e.value),
                        ),
                    )

                    # Chip card comes below the select
                    chip_card = ui.column()

                    # Initial rendering of the chips
                    show_manualIncomeChips(
                        card=chip_card,
                        manualIncome=manualIncome,
                        scenario=Scenario.get_itemByName(scenario_select.value),
                    )
