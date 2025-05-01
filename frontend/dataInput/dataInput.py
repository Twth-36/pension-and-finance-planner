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
from frontend.dataInput.dataInputTiles.pillar3aTile.pillar3aTile import (
    show_pillar3aTile,
)
from frontend.dataInput.dataInputTiles.pillar3aPoliceTile.pillar3aPoliceTile import (
    show_pillar3aPoliceTile,
)
from frontend.dataInput.dataInputTiles.pillar3bPoliceTile.pillar3bPoliceTile import (
    show_pillar3bPoliceTile,
)
from frontend.dataInput.dataInputTiles.realEstateTile import *
from frontend.dataInput.dataInputTiles.realEstateTile.realEstateTile import (
    show_realEstateTile,
)
from frontend.dataInput.dataInputTiles.scenarioTile import *
from frontend.dataInput.dataInputTiles.taxesTile.taxesTile import show_taxesTile
from frontend.dataInput.dataInputTiles.vestedBenefitTile.vestedBenefitTile import (
    show_vestedBenefitTile,
)


def show_dataInput(main_content):
    main_content.clear()
    # Container column for the data input page
    with main_content:
        with ui.row():
            show_personTile()
            # show_personTile()
            show_scenarioTile()

        # "Vermögen und Schulden" Part
        ui.separator()
        ui.label("Vermögen und Schulden").classes("text-h6 font-bold q-mt-md")
        with ui.row():
            show_freeAssetTile()
            show_realEstateTile()
            show_creditTile()
            show_pensionFundTile()
            show_vestedBenefitTile()
            show_pillar3aTile()
            show_pillar3aPoliceTile()
            show_pillar3bPoliceTile()

        # "Einkommen und Ausgaben" Part
        ui.separator()
        ui.label("Einkommen und Ausgaben").classes("text-h6 font-bold q-mt-md")
        with ui.row():
            show_manualIncomeTile()
            show_manualExpenseTile()

        # "Steuern" Part
        ui.separator()
        ui.label("Steuern").classes("text-h6 font-bold q-mt-md")
        with ui.row():
            show_taxesTile()
            show_manualIncomeTaxPosTile()
