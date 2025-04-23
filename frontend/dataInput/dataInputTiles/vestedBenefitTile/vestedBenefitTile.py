from nicegui import ui
from .vestedBenefitOverview import show_vestedBenefitOverview


def show_vestedBenefitTile():
    # Create a card container for vestedBenefits
    vestedBenefit_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")
    # Initialize by showing the vestedBenefit overview
    show_vestedBenefitOverview(vestedBenefit_card)
    return vestedBenefit_card
