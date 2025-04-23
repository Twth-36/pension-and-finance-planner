from nicegui import ui
from backend.classes.freeAsset import *
from backend.utils.monthYear import *
from frontend.utils import *
from frontend.utils.confDialog import show_confDialog
from frontend.utils.format import formatswiss


def show_freeAssetTile():
    # Create a card container for free assets
    asset_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")

    def show_overview(showdetails=False):
        asset_card.clear()
        with asset_card:

            ui.label("Freies Vermögen").classes("text-h6")

            with ui.expansion(icon="tune", value=showdetails) as detail_ext:
                # **Detail fields (Return Rate and Liquidity Reserve)**
                def update_returnRate(new_rate: float):
                    try:
                        FreeAsset.returnRateInvestCap = new_rate
                    except Exception as e:
                        ui.notify(
                            f"Upps, etwas passte da nicht:  \n{e}", color="negative"
                        )
                    ui.notify("Änderung aktualisiert", color="positive")

                rr_input = (
                    ui.number(
                        label="Erwartete Rendite",
                        value=FreeAsset.returnRateInvestCap,
                        format="%.1f",
                    )
                    .props("suffix=%")
                    .tooltip("Erwartete Rendite auf freies Vermögen p.a.")
                    .bind_visibility_from(detail_ext, "value")
                )
                rr_input.on("blur", lambda: update_returnRate(rr_input.value))

                def update_liqRes(new_reserve: float):
                    try:
                        FreeAsset.liqRes = new_reserve
                    except Exception as e:
                        ui.notify(
                            f"Upps, etwas passte da nicht:  \n{e}", color="negative"
                        )
                    ui.notify("Änderung aktualisiert", color="positive")

                liq_input = (
                    ui.number(label="Liquiditätsreserve", value=FreeAsset.liqRes)
                    .tooltip("Nicht investierbarer Betrag als Reserve")
                    .bind_visibility_from(detail_ext, "value")
                )
                liq_input.on("blur", lambda: update_liqRes(liq_input.value))

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
                    ui.button(icon="add", on_click=lambda: show_freeAsset_form()).props(
                        "flat unelevated"
                    )

                    def edit_action():
                        if len(tbl.selected) != 1:
                            ui.notify("Wähle eine Zeile aus.")
                        else:
                            sel_name = tbl.selected[0]["Name"]
                            asset = FreeAsset.get_itemByName(name=sel_name)
                            show_freeAsset_form(freeAsset=asset)

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
                                show_overview(detail_ext.value)  # preserve toggle state

                    ui.button(icon="delete", on_click=del_action).props(
                        "flat unelevated"
                    )

                    ui.button(icon="refresh", on_click=show_overview).props(
                        "flat unelevated"
                    )

        def show_freeAsset_form(freeAsset=None):
            asset_card.clear()
            with asset_card:
                # Input fields for free asset data
                name_input = ui.input(
                    label="Name*",
                    value=(freeAsset.name if freeAsset else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")
                # Prefill person selection if editing an existing asset
                person_prefill = (
                    freeAsset.person.name if (freeAsset and freeAsset.person) else None
                )
                person_input = ui.select(
                    label="Zugehörigkeit",
                    options=[p.name for p in Person.instanceDic.values()],
                    value=person_prefill,
                    with_input=True,
                )
                base_value_input = ui.number(
                    label="Wert",
                    value=(freeAsset.baseValue if freeAsset else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )

                # Form action buttons (Save/Update and Cancel)
                with ui.row():

                    def save_action():
                        try:
                            if freeAsset:  # Update existing asset
                                if freeAsset.name != name_input.value:
                                    freeAsset.update_name(name_input.value)
                                freeAsset.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )
                                freeAsset.baseValue = base_value_input.value
                            else:  # Create new asset
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if base_value_input.value not in [None, ""]:
                                    params["baseValue"] = base_value_input.value
                                FreeAsset.create(**params)
                            show_overview(detail_ext.value)  # return to overview
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:\n{e}", color="negative"
                            )

                    ui.button("Speichern", on_click=save_action)
                    ui.button(
                        "Abbrechen", on_click=lambda: show_overview(detail_ext.value)
                    ).props("outline")

    show_overview()  # Show overview by default

    return asset_card
