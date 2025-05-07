from nicegui import ui
from frontend.dataInput import *
from frontend.dataInput.dataInput import show_dataInput
from frontend.finPlan.finPlan import show_finPlan
from frontend.startPage.startPage import show_startPage
from frontend.taxOverview.taxOverview import show_taxOverview
from frontend.utils.planningProcess import show_planningProcess
from frontend.utils.storageManager import save_all_classes
from frontend.wealthOverview.wealthOverview import show_wealthOverview


# Create left drawer (sidebar) with modern styling.
left_drawer = ui.left_drawer(fixed=True).style(
    "background-color: #fafafa; border-right: 1px solid #ddd; padding: 16px;"
)
with left_drawer:
    ui.label("Navigation").classes("text-h6")

    ui.button("Start", on_click=lambda: show_startPage(main_content)).classes(
        "w-full text-left bg-gray-200 text-black normal-case transition-shadow duration-300 hover:shadow-lg q-pa-sm"
    ).props("flat")

    ui.button("Dateneingabe", on_click=lambda: show_dataInput(main_content)).classes(
        "w-full text-left bg-gray-200 text-black normal-case transition-shadow duration-300 hover:shadow-lg q-pa-sm"
    ).props("flat")
    ui.button(
        "Vermögensübersicht",
        on_click=lambda: show_wealthOverview(main_content),
    ).classes(
        "w-full text-left bg-gray-200 text-black normal-case transition-shadow duration-300 hover:shadow-lg q-pa-sm"
    ).props(
        "flat"
    )
    ui.button(
        "Steuerübersicht",
        on_click=lambda: show_taxOverview(main_content),
    ).classes(
        "w-full text-left bg-gray-200 text-black normal-case transition-shadow duration-300 hover:shadow-lg q-pa-sm"
    ).props(
        "flat"
    )
    ui.button(
        "Finanzplan",
        on_click=lambda: show_finPlan(main_content),
    ).classes(
        "w-full text-left bg-gray-200 text-black normal-case transition-shadow duration-300 hover:shadow-lg q-pa-sm"
    ).props("flat")


# Header
with ui.header(elevated=True).style(
    "background-color: #616161; padding: 16px; postion:relative;"
) as header:
    with ui.row().classes(
        "items-center justify-between w-full"
    ):  # splits items on left and right side
        # left side
        with ui.row().classes("items-center"):
            # Toggle button on the left side.
            ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
                "flat color=white"
            )
            # Title using text-h3 for a slightly smaller heading; white text for contrast.
            ui.markdown("Ich plane meine Pensionierung").classes(
                "text-h3 q-ml-md"
            ).style("color: white;")

        # right side
        with ui.row().classes("items-center"):
            ui.button(icon="rocket", on_click=lambda: show_planningProcess()).props(
                "flat color=white"
            ).tooltip("Starte die Berechnung deines Finanzplanes")

            ui.button(icon="save", on_click=save_all_classes).props("flat color=white")

            fs = ui.fullscreen()
            fs_button = ui.button(
                icon="fullscreen",
                on_click=lambda: (
                    fs.toggle(),
                    fs_button.set_icon("fullscreen_exit" if fs.value else "fullscreen"),
                ),
            ).props("flat color=white")


with ui.footer().style("background-color: #616161; padding: 16px;"):
    with ui.column().classes():
        ui.markdown(
            "Jegliche gewerbliche Verwendung ist untersagt. Sämtliche Angaben sind ohne Gewähr.  \nErstellt durch Tim Wüthrich"
        ).classes("text-body2 q-ml-md")


# Main Content Area
main_content = ui.column().classes("w-full h-full")

show_startPage(main_content)


# Run the NiceGUI application.
app = ui.run()
