from nicegui import ui

from backend.classes.scenario import Scenario
from frontend.finPlan.grid.finPlanGrid import show_finPlanGrid


async def show_finPlan(main_content, scenario: Scenario = None):
    main_content.clear()
    with main_content:
        with ui.column().classes("w-full"):
            with ui.card().classes("q-pa-md border hover:!shadow-2xl"):
                with ui.row().classes("items-center gap-2"):
                    ui.label("Finanzplan").classes("text-h6")
                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_finPlan(
                            main_content=main_content,
                            scenario=Scenario.get_itemByName(scenario_input.value),
                        ),
                    ).props("flat unelevated")

                if scenario is None:  # if no scenario is given, choose the first one
                    scenario = next(iter(Scenario.instanceDic.values()))
                scenario_input = ui.select(
                    label="Auswahl Szenario",
                    options=[s.name for s in Scenario.instanceDic.values()],
                    value=scenario.name if scenario else None,
                    with_input=True,
                    on_change=lambda: show_finPlan(
                        main_content=main_content,
                        scenario=Scenario.get_itemByName(scenario_input.value),
                    ),
                )

                if scenario is not None:
                    if scenario.description:
                        ui.markdown(f"*{scenario.description}*")

            if scenario_input.value:
                await show_finPlanDetails(
                    scenario=Scenario.get_itemByName(scenario_input.value)
                )


async def show_finPlanDetails(scenario: Scenario):
    with ui.tabs().classes("w-full") as tabs:
        tabular = ui.tab("Tabulare Darstellung")
        graphical = ui.tab("Graphische Darstellung")
    with ui.tab_panels(tabs, value=tabular).classes("w-full"):
        with ui.tab_panel(tabular) as tabularPanel:

            await show_finPlanGrid(scenario)
        with ui.tab_panel(graphical) as tabularPanel:
            ui.label("Kommt noch")
