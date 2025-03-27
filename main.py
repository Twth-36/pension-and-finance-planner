from nicegui import ui
from frontend.dataInput import *
from frontend.dataInput.dataInput import show_dataInput

# Create left drawer (sidebar) with modern styling.
left_drawer = ui.left_drawer(fixed=False).style(
    "background-color: #fafafa; border-right: 1px solid #ddd; padding: 16px;"
)
with left_drawer:
    ui.label("Navigation").classes("text-h6")
    # Future navigation buttons can be added here.

# Create header with modern design: lighter grey background, padding, and a slightly smaller title.
with ui.header(elevated=True).style(
    "background-color: #616161; padding: 16px; postion:relative;"
) as header:
    with ui.row().classes("items-center"):
        # Toggle button on the left side.
        ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
            "flat color=white"
        )
        # Title using text-h3 for a slightly smaller heading; white text for contrast.
        ui.markdown("Finanz- und Pensionierungsplaner *by Tim*").classes(
            "text-h3 q-ml-md"
        ).style("color: white;")
with ui.footer().style("background-color: #616161; padding: 16px;"):
    with ui.row().classes("items-center"):
        ui.markdown(
            "Jegliche gewerbliche Verwendung von Dritten ist untersagt!"
        ).classes("text-body2 q-ml-md")
        # Optionally, add elements on the right side here (e.g. user avatar).


# Render the main content by calling your data input form.
show_dataInput()

# Run the NiceGUI application.
ui.run()
