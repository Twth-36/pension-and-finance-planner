from nicegui import ui
from backend.classes.planningobject import Planningobject
from backend.classes.scenario import *
from backend.utils.copyScenario import copyAllFromScenario
from backend.utils.monthYear import *
from frontend.utils import *
from frontend.utils.confDialog import show_confDialog


def show_scenarioTile():
    # Create a card container for the person tile
    scenario_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")

    # Nested function to display the overview table in this card
    def show_overview(showdetails=False):
        scenario_card.clear()
        with scenario_card:

            ui.label("Szenarien").classes("text-h6")
            with ui.expansion(icon="tune", value=showdetails) as detail_ext:

                # **Detail fields (base date and end date)**
                def update_baseDate(new_baseDate: MonthYear):
                    try:
                        Scenario.baseDate = new_baseDate
                    except Exception as e:
                        ui.notify(
                            f"Upps, etwas passte da nicht:  \n{e}",
                            color="negative",
                        )
                    ui.notify("Änderung aktualisiert", color="positive")

                baseDate_input = ui.input(
                    label="Basismonat",
                    value=Scenario.baseDate.dateToString() or "",
                    placeholder="MM.JJJJ",
                    validation={
                        "Format nicht korrekt": lambda v: MonthYear.validate_dateFormat(
                            v
                        )
                    },
                ).tooltip(
                    "Der Basismonat in welchem der Status quo erfasst wurde und ab welchem die Planung startet."
                )
                baseDate_input.on(
                    "blur",
                    lambda: update_baseDate(
                        MonthYear.stringToDate(baseDate_input.value)
                    ),
                )

                def update_endDate(new_endDate: MonthYear):
                    try:
                        Scenario.endDate = new_endDate
                    except Exception as e:
                        ui.notify(
                            f"Upps, etwas passte da nicht:  \n{e}",
                            color="negative",
                        )
                    ui.notify("Änderung aktualisiert", color="positive")

                endDate_input = ui.input(
                    label="Planungsende",
                    value=Scenario.endDate.dateToString() or "",
                    placeholder="MM.JJJJ",
                    validation={
                        "Format nicht korrekt": lambda v: MonthYear.validate_dateFormat(
                            v
                        )
                    },
                ).tooltip(
                    "Definiert bis zu welchem Enddatum die Planung erfolgen soll."
                )
                endDate_input.on(
                    "blur",
                    lambda: update_endDate(MonthYear.stringToDate(endDate_input.value)),
                )

            # Content column (table and controls)
            with ui.column():
                # **Table of Person entries**
                rows = [{"Name": item.name} for item in Scenario.instanceDic.values()]
                columns = [
                    {
                        "name": "Name",
                        "label": "Name",
                        "field": "Name",
                        "align": "center",
                    },
                ]
                tbl = ui.table(
                    columns=columns, rows=rows, row_key="Name", selection="multiple"
                ).style("border: none; background-color: transparent;")

                # **Action buttons (Add, Edit, Delete, Refresh)**
                with ui.row().classes("items-center q-mb-sm"):
                    ui.button(icon="add", on_click=lambda: show_scenario_form()).props(
                        "flat unelevated"
                    )

                    def edit_action():
                        if len(tbl.selected) != 1:
                            ui.notify("Wähle eine Zeile aus.")
                        else:
                            selected_name = tbl.selected[0]["Name"]
                            scenario = Scenario.get_itemByName(name=selected_name)
                            show_scenario_form(scenario=scenario)

                    ui.button(icon="edit", on_click=edit_action).props(
                        "flat unelevated"
                    )

                    def copy_action():
                        if len(tbl.selected) != 1:
                            ui.notify("Wähle eine Zeile aus.")
                        else:
                            selected_name = tbl.selected[0]["Name"]
                            src_scenario = Scenario.get_itemByName(name=selected_name)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            new_scenario = Scenario.create(
                                name=src_scenario.name + "_KOPIE_" + timestamp
                            )

                            copyAllFromScenario(
                                new_scenario=new_scenario, src_scenario=src_scenario
                            )
                            show_scenario_form(scenario=new_scenario)

                    ui.button(icon="content_copy", on_click=copy_action).props(
                        "flat unelevated"
                    ).tooltip("Erstellt eine Kopie des ausgewählten Szenarios")

                    async def del_action():
                        if len(tbl.selected) == 0:
                            ui.notify("Wähle mindestens eine Zeile aus.")
                        else:
                            if await show_confDialog():
                                for item in tbl.selected:
                                    Scenario.get_itemByName(item["Name"]).delete_item()
                                ui.notify("Gelöscht", color="positive")
                                # Refresh overview, preserving detail toggle state
                                show_overview(detail_ext.value)

                    ui.button(icon="delete", on_click=del_action).props(
                        "flat unelevated"
                    )

                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_overview(detail_ext.value),
                    ).props("flat unelevated")

        # Nested function to display the person form in this card
        def show_scenario_form(scenario=None):
            scenario_card.clear()
            with scenario_card:

                # Input fields for person data
                name_input = ui.input(
                    label="Name*",
                    value=(scenario.name if scenario else None),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")

                descr_input = ui.textarea(
                    label="Beschreibung",
                    value=scenario.description if scenario else None,
                )

                # Form action buttons (Save/Update and Cancel)
                with ui.row():

                    def save_action():
                        try:
                            if scenario:  # Update existing person
                                if scenario.name != name_input.value:
                                    scenario.update_name(name_input.value)
                                scenario.description = descr_input.value
                            else:  # Create new person
                                Scenario.create(
                                    name=name_input.value, description=descr_input.value
                                )
                            show_overview(
                                detail_ext.value
                            )  # Return to overview after saving
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:\n{e}",
                                color="negative",
                            )

                    ui.button("Speichern", on_click=save_action)
                    ui.button(
                        "Abbrechen",
                        on_click=lambda: show_overview(detail_ext.value),
                    ).props("outline")

    show_overview()  # Display the overview in the card initially

    return scenario_card
