from nicegui import ui

from backend.classes.freeAsset import FreeAsset
from backend.classes.income import Income
from frontend.utils.manageIncome import dialog_Income


def show_freeAssetDetails(freeAsset_card):
    with ui.column():
        # **Detail fields (Return Rate and Liquidity Reserve)**
        def update_returnRate(new_rate: float):
            try:
                FreeAsset.returnRateInvestCap = new_rate
            except Exception as e:
                ui.notify(f"Upps, etwas passte da nicht:  \n{e}", color="negative")
            ui.notify("Änderung aktualisiert", color="positive")

        rr_input = (
            ui.number(
                label="Erwartete Rendite",
                value=FreeAsset.returnRateInvestCap,
                format="%.1f",
            )
            .props("suffix=%")
            .tooltip("Erwartete Rendite auf freies Vermögen p.a.")
        )
        rr_input.on("blur", lambda: update_returnRate(rr_input.value))

        def update_liqRes(new_reserve: float):
            try:
                FreeAsset.liqRes = new_reserve
            except Exception as e:
                ui.notify(f"Upps, etwas passte da nicht:  \n{e}", color="negative")
            ui.notify("Änderung aktualisiert", color="positive")

        liq_input = ui.number(
            label="Liquiditätsreserve", value=FreeAsset.liqRes
        ).tooltip("Nicht investierbarer Betrag als Reserve")
        liq_input.on("blur", lambda: update_liqRes(liq_input.value))

        # Income-Position return
        # needed functions
        def update_returnIncome(change):
            try:
                FreeAsset.returnIncome = Income.get_itemByName(change.value)
            except Exception as e:
                ui.notify(
                    f"Upps, etwas passte da nicht:  \n{e}",
                    color="negative",
                )
            ui.notify("Änderung gespeichert", color="positive")

        async def edit_returnIncome():
            try:
                if await dialog_Income(FreeAsset.returnIncome):
                    show_freeAssetOverview(freeAsset_card)
            except Exception as e:
                ui.notify(
                    f"Upps, etwas passte da nicht:  \n{e}",
                    color="negative",
                )

        async def new_returnIncome():
            try:
                new_income = await dialog_Income()
                if new_income:
                    FreeAsset.returnIncome = new_income
                show_freeAssetOverview(freeAsset_card)
            except Exception as e:
                ui.notify(
                    f"Upps, etwas passte da nicht:  \n{e}",
                    color="negative",
                )

        # Use local import to avoid circular dependency
        from .freeAssetOverview import show_freeAssetOverview

        with ui.row().classes("items-center gap-2"):

            ui.select(
                label="Einkommen aus Kapital",
                options=[e.name for e in Income.instanceDic.values()],
                value=FreeAsset.returnIncome.name if FreeAsset.returnIncome else None,
                with_input=True,
                on_change=update_returnIncome,
            ).tooltip(
                "Einkommensposition über welche der Ertrag aus investiertem Kapital verrechnet wird."
            )

            ui.button(
                icon="edit",
                on_click=edit_returnIncome,
            ).props(
                "flat unelevated"
            ).tooltip("Einkommensposition bearbeiten")

            ui.button(icon="add", on_click=new_returnIncome).props(
                "flat unelevated"
            ).tooltip("Neue Einkommensposition erstellen")
