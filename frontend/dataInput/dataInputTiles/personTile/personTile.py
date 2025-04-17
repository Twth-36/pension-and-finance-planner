from nicegui import ui
from .personOverview import show_personOverview


def show_personTile():
    # Create a card container
    person_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the overview
    show_personOverview(person_card)
    return person_card
