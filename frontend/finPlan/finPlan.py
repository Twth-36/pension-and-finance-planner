from nicegui import ui


def show_finPlan(main_content):
    main_content.clear()
    with main_content:
        with ui.row():
            ui.icon("minimize")
