from nicegui import ui
from backend.classes.monthYear import MonthYear
from backend.classes.person import Person
from backend.classes.pensionFund import PensionFund
from backend.classes.scenario import Scenario
from frontend.dataInput.dataInputTiles.pensionFundTile.pensionFundDetails import (
    show_pensionFundDetail,
)
from .pensionFundChips import show_pensionFundChips
from frontend.utils import *


def show_pensionFundForm(pensionFund_card, pensionFund=None):
    pensionFund_card.clear()
    with pensionFund_card:
        with ui.row():
            with ui.column():
                # Input fields for data
                name_input = ui.input(
                    label="Name*",
                    value=(pensionFund.name if pensionFund else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")
                person_prefill = (
                    pensionFund.person.name
                    if (pensionFund and pensionFund.person)
                    else None
                )
                person_input = ui.select(
                    label="Zugehörigkeit*",
                    options=[p.name for p in Person.instanceDic.values()],
                    value=person_prefill,
                    with_input=True,
                )
                base_val_input = ui.number(
                    label="Wert",
                    value=(pensionFund.baseValue if pensionFund else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                ).tooltip("Altersguthaben per Planungsbeginn")
                returnRate_input = (
                    ui.number(
                        label="Erwartete Rendite",
                        value=(pensionFund.returnRate if pensionFund else None),
                        format="%.2f",
                    )
                    .props("suffix=%")
                    .tooltip(
                        "Satz zu welchem das Pensionskassenkapital in der Planung verzinst werden soll."
                    )
                )

                baseSaving_input = ui.number(
                    label="Sparbeitrag (pro Monat)",
                    value=(pensionFund.baseSavingContribution if pensionFund else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                ).tooltip(
                    "Sparbeitrag, welcher monatlich dem Pensionskassenkapital zugerechnet wird."
                )

                with ui.row():

                    def save_action():
                        try:
                            if pensionFund:  # Update existing
                                if pensionFund.name != name_input.value:
                                    pensionFund.update_name(name_input.value)
                                pensionFund.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if base_val_input.value:
                                    pensionFund.baseValue = base_val_input.value
                                if returnRate_input.value:
                                    pensionFund.returnRate = returnRate_input.value
                                if baseSaving_input.value:
                                    pensionFund.baseSavingContribution = (
                                        baseSaving_input.value
                                    )
                            else:  # Create new object
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if base_val_input.value:
                                    params["baseValue"] = base_val_input.value
                                if returnRate_input.value:
                                    params["returnRate"] = returnRate_input.value
                                if baseSaving_input.value:
                                    params["baseSavingContribution"] = (
                                        baseSaving_input.value
                                    )
                                new_pensionFund = PensionFund.create(**params)
                            # Refresh the form with updated object
                            if pensionFund:
                                show_pensionFundForm(pensionFund_card, pensionFund)
                            else:
                                show_pensionFundForm(
                                    pensionFund_card, pensionFund=new_pensionFund
                                )
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:\n{e}", color="negative"
                            )

                    btn_label = "Aktualisieren" if pensionFund else "Speichern"
                    ui.button(btn_label, on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .pensionFundOverview import show_pensionFundOverview

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_pensionFundOverview(pensionFund_card),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_pensionFundForm(
                            pensionFund_card, pensionFund
                        ),
                    ).props("flat unelevated")

            if pensionFund and Scenario.instanceDic:

                with ui.column():

                    # Scenario-Selection for chips
                    scenario_select = ui.select(
                        label="Szenario",
                        options=[s.name for s in Scenario.instanceDic.values()],
                        value=next(s.name for s in Scenario.instanceDic.values()),
                        with_input=False,
                        on_change=lambda e: show_pensionFundChips(
                            card=chip_card,  # ← this works because chip_card is defined in the same scope
                            pensionFund=pensionFund,
                            scenario=Scenario.get_itemByName(e.value),
                        ),
                    )

                    # Chip card comes below the select
                    chip_card = ui.column()

                    # Initial rendering of the chips
                    show_pensionFundChips(
                        card=chip_card,
                        pensionFund=pensionFund,
                        scenario=Scenario.get_itemByName(scenario_select.value),
                    )

            # Detail-options
            if pensionFund:
                detail_card = ui.column()
                show_pensionFundDetail(card=detail_card, pensionFund=pensionFund)
