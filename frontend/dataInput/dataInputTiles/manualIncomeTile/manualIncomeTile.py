from nicegui import ui
from .manualIncomeOverview import show_manualIncomeOverview


def show_manualIncomeTile():
    # Create a card container
    manualIncome_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the overview
    show_manualIncomeOverview(manualIncome_card)
    return manualIncome_card
