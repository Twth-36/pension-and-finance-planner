from nicegui import ui
from backend.classes.freeAsset import *
from backend.classes.monthYear import *
from frontend.utils import *

# Global container that will hold either the table or the form.
main_container = ui.card().classes("q-pa-md ")


def show_overview(showdetails=False):
    main_container.clear()
    with main_container:
        with ui.row().classes("justify-center items-center"):
            ui.label("Freie Vermögenswerte").classes("text-h6")
            detail_switch = ui.switch("Details:", value=showdetails).props("left-label")

        with ui.column().classes("q-mt-md"):

            # class variables:
            ## return Rate:
            def update_returnRate(new_returnRate: float):
                try:
                    FreeAsset.returnRateInvestCap = new_returnRate
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht: {e}", color="negative")
                ui.notify("Änderung aktualisiert", color="positive")

            returnRate_input = (
                ui.number(
                    label="Erwartete Rendite",
                    value=(FreeAsset.returnRateInvestCap),
                    format="%.1f",
                )
                .props("suffix=%")
                .tooltip("Gibt die erwartete Rendite auf dem freien Vermögen p.a. an.")
                .bind_visibility_from(detail_switch, "value")
            )
            returnRate_input.on(
                "blur", lambda: update_returnRate(returnRate_input.value)
            )

            ## liquidity reserve
            def update_liqRes(new_liqRes: float):
                try:
                    FreeAsset.liqRes = new_liqRes
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht: {e}", color="negative")
                ui.notify("Änderung aktualisiert", color="positive")

            liqRes_input = (
                ui.number(
                    label="Liquidiätsreserve",
                    value=FreeAsset.liqRes,
                )
                .tooltip(
                    "Gilt als Liquiditätsreserve, welche nicht als investierbares Kapital betrachtet wird."
                )
                .bind_visibility_from(detail_switch, "value")
            )
            liqRes_input.on("blur", lambda: update_liqRes(liqRes_input.value))

            ## table with items:
            rows = []
            for item in FreeAsset.instanceDic.values():
                rows.append(
                    {
                        "Name": item.name,
                        "Zugehörigkeit": item.person.name if item.person else "",
                        "Betrag": item.baseValue,
                    }
                )
            col_defs = [
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
                columns=col_defs, rows=rows, row_key="Name", selection="multiple"
            ).style("border: none; background-color: transparent;")

            ## buttons for editing
            with ui.row().classes("items-center q-mb-sm"):
                ui.button(icon="add", on_click=show_freeAsset_form)

                def edit_action():
                    if len(tbl.selected) != 1:
                        ui.notify("Wähle eine Zeile aus.")
                    else:
                        show_freeAsset_form(
                            freeAsset=FreeAsset.get_itemByName(
                                name=tbl.selected[0]["Name"]
                            )
                        )

                ui.button(icon="edit", on_click=edit_action)

                async def del_action():
                    if len(tbl.selected) == 0:
                        ui.notify("Wähle mindestens eine Zeile aus.")
                    else:
                        if await show_confDialog():
                            for item in tbl.selected:
                                FreeAsset.get_itemByName(item["Name"]).delete_item()

                            ui.notify("Gelöscht", color="positive")
                            show_overview(detail_switch.value)

                ui.button(icon="delete", on_click=del_action)


def show_freeAsset_form(freeAsset=None):
    main_container.clear()
    with main_container:

        name_input = ui.input(
            label="Name*",
            value=freeAsset.name if freeAsset else "",
            validation={"Darf nicht leer sein": lambda value: len(value) > 0},
        ).props("autofocus")
        person_input = ui.select(
            label="Zugehörigkeit",
            options=[item.name for item in Person.instanceDic.values()],
            value=freeAsset.person.name if freeAsset else None,
            with_input=True,
        )
        baseValue_input = ui.number(
            label="Wert",
            value=freeAsset.baseValue if freeAsset else None,
            validation={"Muss grösser oder gleich 0 sein": lambda value: value >= 0},
        )

        with ui.row().classes("q-mt-md"):

            def save_action():
                try:

                    if freeAsset:
                        if freeAsset.name != name_input.value:
                            freeAsset.update_name(name_input.value)
                        freeAsset.person = Person.get_itemByName(person_input.value)
                        freeAsset.baseValue = baseValue_input.value
                    else:
                        param = {"name": name_input.value}
                        if person_input.value not in [None, ""]:
                            param["person"] = Person.get_itemByName(person_input.value)
                        if baseValue_input.value not in [None, ""]:
                            param["baseValue"] = baseValue_input.value
                        FreeAsset.create(**param)
                    show_overview()
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht: \n {e}", color="negative")

            btn_label = "Aktualisieren" if freeAsset else "Speichern"
            ui.button(btn_label, on_click=save_action)
            ui.button("Abbrechen", on_click=show_overview).props("outline")


def show_freeAssetTile():
    pong = Person.create(
        name="Pong", birth=MonthYear(month=1, year=12), conf=Confession.roem_kath
    )
    FreeAsset.create(
        name="Konto",
        person=pong,
    )
    show_overview()
