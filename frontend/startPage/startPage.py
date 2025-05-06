from nicegui import ui

from frontend.showPurposes.examplePlans import handle_load_example
from frontend.utils.storageManager import handle_upload


def show_startPage(main_content):
    main_content.clear()
    # Container column for the data input page
    with main_content:
        with ui.tabs().classes("w-full") as tabs:
            continuePlan = ui.tab("Ich möchte an einem bestehenden Plan weiterarbeiten")
            newPlan = ui.tab("Ich starte eine neuen Plan")
            examplePlan = ui.tab("Zeig mir ein Beispiel")
        with ui.tab_panels(tabs, value=newPlan).classes("w-full"):

            with ui.tab_panel(continuePlan) as continuePlanPanel:
                ui.label("Lade hier deine JSON-Datei vom letzten Mal hoch")
                ui.upload(label="Upload", on_upload=handle_upload)

            with ui.tab_panel(newPlan) as newPlanPanel:
                ui.label("Gehe zu 'Dateneingabe'")

            with ui.tab_panel(examplePlan) as examplePlanPanel:
                ui.button(
                    "Ein verheiratetes Paar kurz vor der Pensionierung",
                    on_click=lambda: handle_load_example("beforePension.json"),
                ).classes(
                    "w-full text-left bg-gray-200 text-black normal-case transition-shadow duration-300 hover:shadow-lg q-pa-sm"
                ).props(
                    "flat"
                )
