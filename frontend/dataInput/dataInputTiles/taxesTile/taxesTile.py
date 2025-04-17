from nicegui import ui

from frontend.dataInput.dataInputTiles.taxesTile.taxesOverview import show_taxesOverview


def show_taxesTile():
    # Create a card container
    taxes_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the overview
    show_taxesOverview(taxes_card)
    return taxes_card
