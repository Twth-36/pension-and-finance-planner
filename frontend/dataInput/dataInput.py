from frontend.dataInput.dataInputTiles.creditTile import *
from frontend.dataInput.dataInputTiles.creditTile.creditTile import show_creditTile
from frontend.dataInput.dataInputTiles.freeAssetTile import *
from frontend.dataInput.dataInputTiles.manualExpenseTile.manualExpenseTile import *
from frontend.dataInput.dataInputTiles.manualIncomeTaxPosTile.manualIncomeTaxPosTile import (
    show_manualIncomeTaxPosTile,
)
from frontend.dataInput.dataInputTiles.manualIncomeTile import *
from nicegui import ui


from frontend.dataInput.dataInputTiles.manualIncomeTile.manualIncomeTile import (
    show_manualIncomeTile,
)
from frontend.dataInput.dataInputTiles.pensionFundTile.pensionFundTile import (
    show_pensionFundTile,
)
from frontend.dataInput.dataInputTiles.personTile import *

from frontend.dataInput.dataInputTiles.personTile.personTile import show_personTile
from frontend.dataInput.dataInputTiles.realEstateTile import *
from frontend.dataInput.dataInputTiles.realEstateTile.realEstateTile import (
    show_realEstateTile,
)
from frontend.dataInput.dataInputTiles.scenarioTile import *
from frontend.dataInput.dataInputTiles.taxesTile.taxesTile import show_taxesTile


def show_dataInput(main_content):
    main_content.clear()
    # Container column for the data input page
    with main_content:
        with ui.row():
            show_personTile()
            # show_personTile()
            show_scenarioTile()

        # "Vermögen und Schulden" Part
        ui.label("Vermögen und Schulden").classes("text-h6 font-bold q-mt-md")
        with ui.row():
            show_freeAssetTile()  # place free assets card
            show_realEstateTile()
            show_creditTile()  # place credits card
            show_pensionFundTile()

        # "Einkommen und Ausgaben" Part
        ui.label("Einkommen und Ausgaben").classes("text-h6 font-bold q-mt-md")
        with ui.row():
            show_manualIncomeTile()
            show_manualExpenseTile()
        ui.label("Steuern").classes("text-h6 font-bold q-mt-md")
        with ui.row():
            show_taxesTile()
            show_manualIncomeTaxPosTile()
