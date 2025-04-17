from nicegui import ui

from backend.classes.pensionFund import PensFundPayoutPos, PensionFund
from backend.classes.planningposition import *


def dialog_pensFundPayoutPos(
    payoutPosList: List[PensFundPayoutPos],
    payoutPos: PensFundPayoutPos = None,
    scenario: Scenario = None,
):
    with ui.dialog() as dialog, ui.card():

        scenario_prefill = None
        if payoutPos:
            if payoutPos.scenario:
                scenario_prefill = payoutPos.scenario.name
        elif scenario:
            scenario_prefill = scenario.name
        scenario_input = ui.select(
            label="Szenario*",
            options=[s.name for s in Scenario.instanceDic.values()],
            value=scenario_prefill,
            with_input=True,
        )

        period_prefill = None
        if payoutPos:
            if payoutPos.period:
                period_prefill = payoutPos.period.dateToString()
        period_input = (
            ui.input(
                label="Monat",
                placeholder="MM.JJJJ",
                validation={
                    "Format nicht korrekt": lambda v: MonthYear.validate_dateFormat(v)
                },
                value=period_prefill,
            )
            .tooltip("Zeitpunkt der (Teil-)Pensionierung")
            .props("autofocus")
        )

        value_input = (
            ui.number(
                label="Pensionierungsumfang",
                value=payoutPos.value if payoutPos else 0,
            )
            .props("suffix=%")
            .tooltip(
                "Höhe der Pensumsreduktion im Verhältnis zum vorangehenden Pensum. Bsp. Teilpensionierung im Jahr 20x1 und 20x2 von je 50% --> 20x1: 50%, 20x2: 100%"
            )
        )

        capitalPortion_input = (
            ui.number(
                label="Anteil Kapitalbezug",
                value=payoutPos.capitalPortion if payoutPos else 0,
            )
            .props("suffix=%")
            .tooltip(
                "Anteil vom relevanten Alterskapital, welches als Kapital ausbezahlt wird. Der Restbetrag wird als Rente ausbezahlt."
            )
        )

        conversionRate_input = (
            ui.number(
                label="Umwandlungssatz",
                value=payoutPos.conversionRate if payoutPos else 0,
            )
            .props("suffix=%")
            .tooltip(
                "Prozentsatz des relevanten Alterskapitals, welcher als jährliche Rente ausbezahlt wird."
            )
        )

        desc_input = ui.input(
            label="Beschreibung", value=payoutPos.description if payoutPos else None
        ).tooltip("Eine kleine Erinnerung um die Planung nachvollziehen zu können.")

        inDoc_input = ui.checkbox(
            text="In Dokumentation", value=payoutPos.inDoc if payoutPos else False
        )

        with ui.row():

            def save_action():
                try:
                    if payoutPos:  # update existing
                        payoutPos.update(
                            list=payoutPosList,
                            new_scenario=Scenario.get_itemByName(scenario_input.value),
                            new_period=MonthYear.stringToDate(period_input.value),
                            new_value=value_input.value,
                            new_inDoc=inDoc_input.value,
                            new_description=desc_input.value,
                            new_capitalPortion=capitalPortion_input.value,
                            new_conversionRate=conversionRate_input.value,
                        )

                    else:  # create new payoutPos
                        PensFundPayoutPos(
                            scenario=Scenario.get_itemByName(scenario_input.value),
                            period=MonthYear.stringToDate(period_input.value),
                            value=value_input.value,
                            inDoc=inDoc_input.value,
                            description=desc_input.value,
                            capitalPortion=capitalPortion_input.value,
                            conversionRate=conversionRate_input.value,
                        ).add_toList(payoutPosList)

                    dialog.submit(True)

                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:\n{e}",
                        color="negative",
                    )

            ui.button(
                "Aktualisieren" if payoutPos else "Speichern", on_click=save_action
            )

            ui.button("Abbrechen", on_click=lambda: dialog.submit(None)).props(
                "outline"
            )
    return dialog
