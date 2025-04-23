from nicegui import ui
from .pillar3bPoliceOverview import show_pillar3bPoliceOverview


def show_pillar3bPoliceTile():
    # Create a card container for pillar3bPolices
    pillar3bPolice_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the pillar3bPolice overview
    show_pillar3bPoliceOverview(pillar3bPolice_card)
    return pillar3bPolice_card
