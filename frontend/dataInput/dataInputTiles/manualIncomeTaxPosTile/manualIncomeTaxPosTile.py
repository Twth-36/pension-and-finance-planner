from nicegui import ui

from frontend.dataInput.dataInputTiles.manualIncomeTaxPosTile.manualIncomeTaxPosOverview import (
    show_manualIncomeTaxPosOverview,
)


def show_manualIncomeTaxPosTile():
    # Create a card container
    manualIncomeTaxPos_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the overview
    show_manualIncomeTaxPosOverview(manualIncomeTaxPos_card)
    return manualIncomeTaxPos_card
