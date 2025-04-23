from nicegui import ui
from backend.classes.vestedBenefit import VestedBenefit, Person
from backend.utils.monthYear import MonthYear
from backend.classes.realEstate import *
from frontend.dataInput.dataInputTiles.vestedBenefitTile.vestedBenefitDetails import (
    show_vestedBenefitDetail,
)

from .vestedBenefitChips import show_vestedBenefitChips
from frontend.utils import *


def show_vestedBenefitForm(vestedBenefit_card, vestedBenefit=None):
    vestedBenefit_card.clear()
    with vestedBenefit_card:
        with ui.row():
            with ui.column():
                # Input fields for vestedBenefit data
                name_input = ui.input(
                    label="Name*",
                    value=(vestedBenefit.name if vestedBenefit else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")

                person_prefill = (
                    vestedBenefit.person.name
                    if (vestedBenefit and vestedBenefit.person)
                    else None
                )
                person_input = ui.select(
                    label="Zugehörigkeit*",
                    options=[p.name for p in Person.instanceDic.values()],
                    value=person_prefill,
                    with_input=True,
                )
                baseValue_input = ui.number(
                    label="Wert",
                    value=(vestedBenefit.baseValue if vestedBenefit else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )
                returnRate_input = ui.number(
                    label="Erwartete Rendite",
                    value=(vestedBenefit.returnRate if vestedBenefit else None),
                    format="%.2f",
                ).props("suffix=%")

                with ui.row():

                    def save_action():
                        try:
                            if vestedBenefit:  # Update existing
                                if vestedBenefit.name != name_input.value:
                                    vestedBenefit.update_name(name_input.value)
                                vestedBenefit.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if baseValue_input.value:
                                    vestedBenefit.baseValue = baseValue_input.value
                                if returnRate_input.value:
                                    vestedBenefit.returnRate = returnRate_input.value

                            else:  # Create new vestedBenefit
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if baseValue_input.value:
                                    params["baseValue"] = baseValue_input.value
                                if returnRate_input.value:
                                    params["returnRate"] = returnRate_input.value

                                new_vestedBenefit = VestedBenefit.create(**params)
                            # Refresh the form with updated vestedBenefit
                            if vestedBenefit:
                                show_vestedBenefitForm(
                                    vestedBenefit_card, vestedBenefit
                                )
                            else:
                                show_vestedBenefitForm(
                                    vestedBenefit_card, vestedBenefit=new_vestedBenefit
                                )
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:  \n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .vestedBenefitOverview import show_vestedBenefitOverview

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_vestedBenefitOverview(vestedBenefit_card),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_vestedBenefitForm(
                            vestedBenefit_card, vestedBenefit
                        ),
                    ).props("flat unelevated")

            if vestedBenefit and Scenario.instanceDic:

                with ui.column():

                    # Scenario-Selection for chips
                    scenario_select = ui.select(
                        label="Szenario",
                        options=[s.name for s in Scenario.instanceDic.values()],
                        value=next(s.name for s in Scenario.instanceDic.values()),
                        with_input=False,
                        on_change=lambda e: show_vestedBenefitChips(
                            card=chip_card,  # ← this works because chip_card is defined in the same scope
                            vestedBenefit=vestedBenefit,
                            scenario=Scenario.get_itemByName(e.value),
                        ),
                    )

                    # Chip card comes below the select
                    chip_card = ui.column()

                    # Initial rendering of the chips
                    show_vestedBenefitChips(
                        card=chip_card,
                        vestedBenefit=vestedBenefit,
                        scenario=Scenario.get_itemByName(scenario_select.value),
                    )

            # Detail-options
            if vestedBenefit:
                detail_card = ui.column()
                show_vestedBenefitDetail(card=detail_card, vestedBenefit=vestedBenefit)
