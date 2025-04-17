from nicegui import ui
from .pensionFundOverview import show_pensionFundOverview


def show_pensionFundTile():
    # Create a card container
    pensionFund_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the overview
    show_pensionFundOverview(pensionFund_card)
    return pensionFund_card
