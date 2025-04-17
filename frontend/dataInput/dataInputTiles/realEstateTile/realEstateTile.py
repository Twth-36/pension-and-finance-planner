from nicegui import ui
from .realEstateOverview import show_realEstateOverview


def show_realEstateTile():
    # Create a card container
    realEstate_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the overview
    show_realEstateOverview(realEstate_card)
    return realEstate_card
