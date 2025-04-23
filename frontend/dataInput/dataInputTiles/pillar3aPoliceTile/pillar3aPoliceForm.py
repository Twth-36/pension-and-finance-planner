from nicegui import ui
from backend.classes.pillar3aPolice import Pillar3aPolice, Person
from backend.utils.monthYear import MonthYear
from backend.classes.realEstate import *
from backend.utils.payFrequency import PayFrequency
from frontend.dataInput.dataInputTiles.pillar3aPoliceTile.pillar3aPoliceDetails import (
    show_pillar3aPoliceDetail,
)

from frontend.utils import *


def show_pillar3aPoliceForm(pillar3aPolice_card, pillar3aPolice=None):
    pillar3aPolice_card.clear()
    with pillar3aPolice_card:
        with ui.row():
            with ui.column():
                # Input fields for pillar3aPolice data
                name_input = ui.input(
                    label="Name*",
                    value=(pillar3aPolice.name if pillar3aPolice else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")

                person_prefill = (
                    pillar3aPolice.person.name
                    if (pillar3aPolice and pillar3aPolice.person)
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
                    value=(pillar3aPolice.baseValue if pillar3aPolice else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )

                with ui.row().classes("justify-center items-center"):
                    deposit_input = ui.number(
                        label="Prämie",
                        value=(pillar3aPolice.deposit if pillar3aPolice else None),
                        validation={
                            "Muss grösser oder gleich 0 sein": lambda v: v is None
                            or v >= 0
                        },
                    ).tooltip(
                        "Zu entrichtende Prämie. Die Einzahlung wird jeweils bis zum Ablauf berücksichtigt."
                    )

                    depositFreq_input = ui.toggle(
                        {PayFrequency.M: "M", PayFrequency.Y: "J"}, value=PayFrequency.Y
                    ).tooltip("M: Monatsprämie, J: Jahresprämie")

                payoutDate_input = ui.input(
                    label="Ablauf*",
                    placeholder="MM.JJJJ",
                    validation={
                        "Format nicht korrekt": lambda v: MonthYear.validate_dateFormat(
                            v
                        )
                    },
                    value=(
                        pillar3aPolice.payoutDate.dateToString()
                        if pillar3aPolice
                        else None
                    ),
                )

                expPayoutValue_input = ui.number(
                    label="Erwarteter Auszahlungswert",
                    value=(pillar3aPolice.expPayoutValue if pillar3aPolice else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                ).tooltip("Der erwartete Auszahlungswert (z.B. Erlebenfallkapital)")

                with ui.row():

                    def save_action():
                        try:
                            if pillar3aPolice:  # Update existing
                                if pillar3aPolice.name != name_input.value:
                                    pillar3aPolice.update_name(name_input.value)
                                pillar3aPolice.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if baseValue_input.value:
                                    pillar3aPolice.baseValue = baseValue_input.value
                                if expPayoutValue_input.value:
                                    pillar3aPolice.expPayoutValue = (
                                        expPayoutValue_input.value
                                    )
                                if payoutDate_input.value:
                                    pillar3aPolice.payoutDate = MonthYear.stringToDate(
                                        payoutDate_input.value
                                    )
                                if deposit_input.value:
                                    pillar3aPolice.deposit = deposit_input.value

                                if depositFreq_input.value:
                                    pillar3aPolice.depositFreq = depositFreq_input.value

                            else:  # Create new pillar3aPolice
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if baseValue_input.value:
                                    params["baseValue"] = baseValue_input.value
                                if expPayoutValue_input.value:
                                    params["expPayoutValue"] = (
                                        expPayoutValue_input.value
                                    )
                                if payoutDate_input.value:
                                    params["payoutDate"] = MonthYear.stringToDate(
                                        payoutDate_input.value
                                    )
                                if deposit_input.value:
                                    params["deposit"] = deposit_input.value
                                if depositFreq_input.value:
                                    params["depositFreq"] = depositFreq_input.value

                                new_pillar3aPolice = Pillar3aPolice.create(**params)
                            # Refresh the form with updated pillar3aPolice
                            if pillar3aPolice:
                                show_pillar3aPoliceForm(
                                    pillar3aPolice_card, pillar3aPolice
                                )
                            else:
                                show_pillar3aPoliceForm(
                                    pillar3aPolice_card,
                                    pillar3aPolice=new_pillar3aPolice,
                                )
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:  \n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .pillar3aPoliceOverview import show_pillar3aPoliceOverview

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_pillar3aPoliceOverview(
                            pillar3aPolice_card
                        ),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_pillar3aPoliceForm(
                            pillar3aPolice_card, pillar3aPolice
                        ),
                    ).props("flat unelevated")

            # Detail-options
            if pillar3aPolice:
                detail_card = ui.column()
                show_pillar3aPoliceDetail(
                    card=detail_card, pillar3aPolice=pillar3aPolice
                )
