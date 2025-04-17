from nicegui import ui
from .manualExpenseOverview import show_manualExpenseOverview


def show_manualExpenseTile():
    # Create a card container
    manualExpense_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the overview
    show_manualExpenseOverview(manualExpense_card)
    return manualExpense_card
