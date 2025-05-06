from nicegui import ui

from frontend.dataInput.dataInputTiles.freeAssetTile.freeAssetOverview import (
    show_freeAssetOverview,
)


def show_freeAssetTile():
    # Create a card container for free assets
    freeAsset_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")

    show_freeAssetOverview(freeAsset_card)  # Show overview by default

    return freeAsset_card
