from frontend.dataInput.dataInputTiles.creditTile import *
from frontend.dataInput.dataInputTiles.freeAssetTile import *
from frontend.dataInput.dataInputTiles.personTile import *
from nicegui import ui


from frontend.dataInput.dataInputTiles.realEstateTile import *
from frontend.dataInput.dataInputTiles.realEstateTile import show_realEstateTile
from frontend.dataInput.dataInputTiles.scenarioTile import *


def show_dataInput():
    # Container column for the data input page
    with ui.column():
        with ui.row():
            show_personTile()  # returns a ui.card component
            show_scenarioTile()

        ui.label("Vermögen und Schulden").classes("text-h6 font-bold q-mt-md")

        # Row with free asset tile and credit tile side by side
        with ui.row():
            show_freeAssetTile()  # place free assets card
            show_realEstateTile.show_realEstateTile()
            show_creditTile.show_creditTile()  # place credits card

        ui.label("Einkommen und Ausgaben").classes("text-h6 font-bold q-mt-md")
        ui.label("Steuern").classes("text-h6 font-bold q-mt-md")
