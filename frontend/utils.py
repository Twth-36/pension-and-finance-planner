from nicegui import ui

from backend.classes.planningposition import *


# confirmation dialog box
def confDialog(message: str = "Bist du sicher?"):
    # Create and return a dialog instance
    with ui.dialog() as dialog, ui.card():
        ui.label(message)
        with ui.row():
            ui.button("Ja", on_click=lambda: dialog.submit(True))
            ui.button("Nein", on_click=lambda: dialog.submit(False)).props("outline")
    return dialog


def dialog_planPos(
    planPosList: List[Planningposition],
    planPos: Planningposition = None,
    scenario: Scenario = None,
    periodLabel: str = "Monat",
    periodTooltip: str = None,
    valueLabel: str = "Wert",
    valueTooltip: str = None,
    valueFormat: str = None,
    valueProps: str = None,
):
    with ui.dialog() as dialog, ui.card():

        scenario_prefill = None
        if planPos:
            if planPos.scenario:
                scenario_prefill = planPos.scenario.name
        elif scenario:
            scenario_prefill = scenario.name
        scenario_input = ui.select(
            label="Szenario*",
            options=[s.name for s in Scenario.instanceDic.values()],
            value=scenario_prefill,
            with_input=True,
        )

        period_prefill = None
        if planPos:
            if planPos.period:
                period_prefill = planPos.period.dateToString()
        period_input = (
            ui.input(
                label=periodLabel + "*",
                placeholder="MM.JJJJ",
                validation={
                    "Format nicht korrekt": lambda v: MonthYear.validate_dateFormat(v)
                },
                value=period_prefill,
            )
            .tooltip(periodTooltip)
            .props("autofocus")
        )

        value_input = (
            ui.number(
                label=valueLabel,
                value=planPos.value if planPos else 0,
                format=valueFormat,
            )
            .props(valueProps)
            .tooltip(valueTooltip)
        )

        desc_input = ui.input(
            label="Beschreibung", value=planPos.description if planPos else None
        ).tooltip("Eine kleine Erinnerung um die Planung nachvollziehen zu können.")

        inDoc_input = ui.checkbox(
            text="In Dokumentation", value=planPos.inDoc if planPos else False
        )

        with ui.row():

            def save_action():
                try:
                    if planPos:  # update existing
                        planPos.update(
                            list=planPosList,
                            new_scenario=Scenario.get_itemByName(scenario_input.value),
                            new_period=MonthYear.stringToDate(period_input.value),
                            new_value=value_input.value,
                            new_inDoc=inDoc_input.value,
                            new_description=desc_input.value,
                        )

                    else:  # create new planPos
                        Planningposition(
                            scenario=Scenario.get_itemByName(scenario_input.value),
                            period=MonthYear.stringToDate(period_input.value),
                            value=value_input.value,
                            inDoc=inDoc_input.value,
                            description=desc_input.value,
                        ).add_toList(planPosList)

                    dialog.submit(True)

                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:\n{e}",
                        color="negative",
                    )

            ui.button("Aktualisieren" if planPos else "Speichern", on_click=save_action)

            ui.button("Abbrechen", on_click=lambda: dialog.submit(None)).props(
                "outline"
            )
    return dialog


def formatswiss(value: float, decimals: int = 0):
    return f"{value:,.{decimals}f}".replace(",", "'")
