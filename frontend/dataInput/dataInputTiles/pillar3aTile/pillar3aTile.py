from nicegui import ui
from .pillar3aOverview import show_pillar3aOverview


def show_pillar3aTile():
    # Create a card container for pillar3as
    pillar3a_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the pillar3a overview
    show_pillar3aOverview(pillar3a_card)
    return pillar3a_card
