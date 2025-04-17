from nicegui import ui


# confirmation dialog box
def show_confDialog(message: str = "Bist du sicher?"):
    # Create and return a dialog instance
    with ui.dialog() as dialog, ui.card():
        ui.label(message)
        with ui.row():
            ui.button("Ja", on_click=lambda: dialog.submit(True))
            ui.button("Nein", on_click=lambda: dialog.submit(False)).props("outline")
    return dialog
