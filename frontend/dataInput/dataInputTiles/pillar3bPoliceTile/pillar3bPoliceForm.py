from nicegui import ui
from backend.classes.pillar3bPolice import Pillar3bPolice, Person
from backend.utils.monthYear import MonthYear
from backend.classes.realEstate import *
from backend.utils.payFrequency import PayFrequency
from frontend.dataInput.dataInputTiles.pillar3bPoliceTile.pillar3bPoliceDetails import (
    show_pillar3bPoliceDetail,
)

from frontend.utils import *


def show_pillar3bPoliceForm(pillar3bPolice_card, pillar3bPolice=None):
    pillar3bPolice_card.clear()
    with pillar3bPolice_card:
        with ui.row():
            with ui.column():
                # Input fields for pillar3bPolice data
                name_input = ui.input(
                    label="Name*",
                    value=(pillar3bPolice.name if pillar3bPolice else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")

                person_prefill = (
                    pillar3bPolice.person.name
                    if (pillar3bPolice and pillar3bPolice.person)
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
                    value=(pillar3bPolice.baseValue if pillar3bPolice else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )

                with ui.row().classes("justify-center items-center"):
                    deposit_input = ui.number(
                        label="Prämie",
                        value=(pillar3bPolice.deposit if pillar3bPolice else None),
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
                        pillar3bPolice.payoutDate.dateToString()
                        if pillar3bPolice
                        else None
                    ),
                )

                expPayoutValue_input = ui.number(
                    label="Erwarteter Auszahlungswert",
                    value=(pillar3bPolice.expPayoutValue if pillar3bPolice else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                ).tooltip("Der erwartete Auszahlungswert (z.B. Erlebenfallkapital)")

                expPensionValue_input = ui.number(
                    label="Erwartete monatliche Rente",
                    value=(pillar3bPolice.expPensionValue if pillar3bPolice else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                ).tooltip("Die erwartete monatliche Rente ab Ablauf.")

                with ui.row():

                    def save_action():
                        try:
                            if pillar3bPolice:  # Update existing
                                if pillar3bPolice.name != name_input.value:
                                    pillar3bPolice.update_name(name_input.value)
                                pillar3bPolice.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )

                                if baseValue_input.value:
                                    pillar3bPolice.baseValue = baseValue_input.value
                                if expPayoutValue_input.value:
                                    pillar3bPolice.expPayoutValue = (
                                        expPayoutValue_input.value
                                    )
                                if expPensionValue_input.value:
                                    pillar3bPolice.expPensionValue = (
                                        expPensionValue_input.value
                                    )
                                if payoutDate_input.value:
                                    pillar3bPolice.payoutDate = MonthYear.stringToDate(
                                        payoutDate_input.value
                                    )
                                if deposit_input.value:
                                    pillar3bPolice.deposit = deposit_input.value

                                if depositFreq_input.value:
                                    pillar3bPolice.depositFreq = depositFreq_input.value

                            else:  # Create new pillar3bPolice
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
                                if expPensionValue_input.value:
                                    params["expPensionValue"] = (
                                        expPensionValue_input.value
                                    )
                                if payoutDate_input.value:
                                    params["payoutDate"] = MonthYear.stringToDate(
                                        payoutDate_input.value
                                    )
                                if deposit_input.value:
                                    params["deposit"] = deposit_input.value
                                if depositFreq_input.value:
                                    params["depositFreq"] = depositFreq_input.value

                                new_pillar3bPolice = Pillar3bPolice.create(**params)
                            # Refresh the form with updated pillar3bPolice
                            if pillar3bPolice:
                                show_pillar3bPoliceForm(
                                    pillar3bPolice_card, pillar3bPolice
                                )
                            else:
                                show_pillar3bPoliceForm(
                                    pillar3bPolice_card,
                                    pillar3bPolice=new_pillar3bPolice,
                                )
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:  \n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    # Use local import to avoid circular dependency
                    from .pillar3bPoliceOverview import show_pillar3bPoliceOverview

                    ui.button(
                        "Schliessen",
                        on_click=lambda: show_pillar3bPoliceOverview(
                            pillar3bPolice_card
                        ),
                    ).props("outline")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_pillar3bPoliceForm(
                            pillar3bPolice_card, pillar3bPolice
                        ),
                    ).props("flat unelevated")

            # Detail-options
            if pillar3bPolice:
                detail_card = ui.column()
                show_pillar3bPoliceDetail(
                    card=detail_card, pillar3bPolice=pillar3bPolice
                )
