from nicegui import ui
from backend.classes.credit import Credit, Person
from backend.utils.monthYear import MonthYear
from backend.classes.realEstate import *
from frontend.dataInput.dataInputTiles.creditTile.creditDetails import show_creditDetail
from .creditChips import show_creditChips
from frontend.utils import *


def show_creditForm(credit_card, credit=None):
    credit_card.clear()
    with credit_card:
        with ui.row():
            with ui.column():
                # Input fields for credit data
                name_input = ui.input(
                    label="Name*",
                    value=(credit.name if credit else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")

                person_prefill = (
                    credit.person.name if (credit and credit.person) else None
                )
                person_input = ui.select(
                    label="Zugehörigkeit",
                    options=[p.name for p in Person.instanceDic.values()],
                    value=person_prefill,
                    with_input=True,
                )
                base_val_input = ui.number(
                    label="Wert",
                    value=(credit.baseValue if credit else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )
                interest_input = ui.number(
                    label="Zinssatz",
                    value=(credit.baseInterestRate if credit else None),
                    format="%.2f",
                ).props("suffix=%")

                endDate_prefill = None
                if credit and credit.endDate:
                    endDate_prefill = credit.endDate.dateToString()
                endDate_input = ui.input(
                    label="Ablaufmonat",
                    placeholder="MM.JJJJ",
                    validation={
                        "Format nicht korrekt": lambda v: MonthYear.validate_dateFormat(
                            v
                        )
                    },
                    value=endDate_prefill,
                )

                realEstate_prefill = (
                    credit.realEstate.name if (credit and credit.realEstate) else None
                )
                realEstate_input = ui.select(
                    label="Liegenschaft",
                    options=[r.name for r in RealEstate.instanceDic.values()],
                    value=realEstate_prefill,
                    with_input=True,
                ).tooltip(
                    "Dazugehörige Liegenschaft falls es sich um eine Hypothek handelt."
                )

                with ui.row():

                    def save_action():
                        try:
                            if credit:  # Update existing
                                if credit.name != name_input.value:
                                    credit.update_name(name_input.value)
                                credit.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if base_val_input.value:
                                    credit.baseValue = base_val_input.value
                                if interest_input.value:
                                    credit.baseInterestRate = interest_input.value
                                if endDate_input.value:
                                    credit.endDate = MonthYear.stringToDate(
                                        endDate_input.value
                                    )
                                if realEstate_input.value:
                                    credit.realEstate = RealEstate.get_itemByName(
                                        realEstate_input.value
                                    )
                            else:  # Create new credit
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if base_val_input.value:
                                    params["baseValue"] = base_val_input.value
                                if interest_input.value:
                                    params["baseInterestRate"] = interest_input.value
                                if endDate_input.value:
                                    params["endDate"] = MonthYear.stringToDate(
                                        endDate_input.value
                                    )
                                if realEstate_input.value:
                                    params["realEstate"] = RealEstate.get_itemByName(
                                        realEstate_input.value
                                    )
                                new_credit = Credit.create(**params)
                            # Refresh the form with updated credit
                            if credit:
                                show_creditForm(credit_card, credit)
                            else:
                                show_creditForm(credit_card, credit=new_credit)
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:  \n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .creditOverview import show_creditOverview

                    ui.button(
                        "Schliessen", on_click=lambda: show_creditOverview(credit_card)
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_creditForm(credit_card, credit),
                    ).props("flat unelevated")

            if credit and Scenario.instanceDic:

                with ui.column():

                    # Scenario-Selection for chips
                    scenario_select = ui.select(
                        label="Szenario",
                        options=[s.name for s in Scenario.instanceDic.values()],
                        value=next(s.name for s in Scenario.instanceDic.values()),
                        with_input=False,
                        on_change=lambda e: show_creditChips(
                            card=chip_card,  # ← this works because chip_card is defined in the same scope
                            credit=credit,
                            scenario=Scenario.get_itemByName(e.value),
                        ),
                    )

                    # Chip card comes below the select
                    chip_card = ui.column()

                    # Initial rendering of the chips
                    show_creditChips(
                        card=chip_card,
                        credit=credit,
                        scenario=Scenario.get_itemByName(scenario_select.value),
                    )

            # Detail-options
            if credit:
                detail_card = ui.column()
                show_creditDetail(card=detail_card, credit=credit)
