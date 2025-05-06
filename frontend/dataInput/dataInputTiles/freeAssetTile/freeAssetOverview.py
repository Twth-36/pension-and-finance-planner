from nicegui import ui

from backend.classes.freeAsset import FreeAsset
from frontend.dataInput.dataInputTiles.freeAssetTile.freeAssetDetails import (
    show_freeAssetDetails,
)
from frontend.dataInput.dataInputTiles.freeAssetTile.freeAssetForm import (
    show_freeAssetForm,
)
from frontend.utils.confDialog import show_confDialog
from frontend.utils.format import formatswiss


def show_freeAssetOverview(freeAsset_card):
    freeAsset_card.clear()
    with freeAsset_card:

        with ui.row().classes("justify-center items-center"):
            ui.label("Freie Vermögenswerte").classes("text-h6")

        with ui.row():

            with ui.column():
                # **Table of FreeAsset entries**
                rows = [
                    {
                        "Name": fa.name,
                        "Zugehörigkeit": (fa.person.name if fa.person else ""),
                        "Betrag": formatswiss(fa.baseValue),
                    }
                    for fa in FreeAsset.instanceDic.values()
                ]
                columns = [
                    {
                        "name": "Name",
                        "label": "Name",
                        "field": "Name",
                        "align": "center",
                    },
                    {
                        "name": "Zugehörigkeit",
                        "label": "Zugehörigkeit",
                        "field": "Zugehörigkeit",
                        "align": "center",
                    },
                    {
                        "name": "Betrag",
                        "label": "Betrag",
                        "field": "Betrag",
                        "align": "center",
                    },
                ]
                tbl = ui.table(
                    columns=columns, rows=rows, row_key="Name", selection="multiple"
                ).style("border: none; background-color: transparent;")

                # **Action buttons (Add, Edit, Delete, Refresh)**
                with ui.row().classes("items-center q-mb-sm"):
                    ui.button(
                        icon="add", on_click=lambda: show_freeAssetForm(freeAsset_card)
                    ).props("flat unelevated")

                    def edit_action():
                        if len(tbl.selected) != 1:
                            ui.notify("Wähle eine Zeile aus.")
                        else:
                            sel_name = tbl.selected[0]["Name"]
                            freeAsset = FreeAsset.get_itemByName(name=sel_name)
                            show_freeAssetForm(
                                freeAsset_card=freeAsset_card, freeAsset=freeAsset
                            )

                    ui.button(icon="edit", on_click=edit_action).props(
                        "flat unelevated"
                    )

                    async def del_action():
                        if len(tbl.selected) == 0:
                            ui.notify("Wähle mindestens eine Zeile aus.")
                        else:
                            if await show_confDialog():
                                for item in tbl.selected:
                                    FreeAsset.get_itemByName(item["Name"]).delete_item()
                                ui.notify("Gelöscht", color="positive")
                                show_freeAssetOverview(
                                    freeAsset_card
                                )  # preserve toggle state

                    ui.button(icon="delete", on_click=del_action).props(
                        "flat unelevated"
                    )

                    ui.button(
                        icon="refresh",
                        on_click=lambda: show_freeAssetOverview(freeAsset_card),
                    ).props("flat unelevated")

            ui.separator().props("vertical")
            with ui.expansion(icon="tune") as detail_ext:
                show_freeAssetDetails(freeAsset_card)
