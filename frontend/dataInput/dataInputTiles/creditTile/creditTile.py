from nicegui import ui
from .creditOverview import show_creditOverview


def show_creditTile():
    # Create a card container for credits
    credit_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the credit overview
    show_creditOverview(credit_card)
    return credit_card
