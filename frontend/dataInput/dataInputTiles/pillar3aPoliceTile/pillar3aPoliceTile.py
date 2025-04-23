from nicegui import ui
from .pillar3aPoliceOverview import show_pillar3aPoliceOverview


def show_pillar3aPoliceTile():
    # Create a card container for pillar3aPolices
    pillar3aPolice_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the pillar3aPolice overview
    show_pillar3aPoliceOverview(pillar3aPolice_card)
    return pillar3aPolice_card
