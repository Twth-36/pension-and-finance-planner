from nicegui import ui


from backend.classes.incomeTaxPos import IncomeTaxPos
from backend.classes.manualExpense import ManualExpense

from frontend.utils.manageIncomeTaxPos import dialog_IncomeTaxPos


def show_manualExpenseDetail(
    card, manualExpense: ManualExpense = None, show_details: bool = False
):
    card.clear()
    with card:
        with ui.expansion(icon="tune", value=show_details) as detail_ext:

            # IncometaxPosition
            # needed functions
            def update_taxPosition(change):
                try:
                    manualExpense.taxPosition = IncomeTaxPos.get_itemByName(
                        change.value
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )
                ui.notify("Änderung gespeichert", color="positive")

            async def edit_taxPosition():
                try:
                    if await dialog_IncomeTaxPos(manualExpense.taxPosition):
                        show_manualExpenseDetail(
                            card=card,
                            manualExpense=manualExpense,
                            show_details=detail_ext.value,
                        )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            async def new_taxPosition():
                try:
                    new_taxPos = await dialog_IncomeTaxPos()
                    if new_taxPos:
                        manualExpense.taxPosition = new_taxPos
                    show_manualExpenseDetail(
                        card=card,
                        manualExpense=manualExpense,
                        show_details=detail_ext.value,
                    )
                except Exception as e:
                    ui.notify(
                        f"Upps, etwas passte da nicht:  \n{e}",
                        color="negative",
                    )

            with ui.row().classes("items-center gap-2"):
                ui.select(
                    label="Steuerposition",
                    options=[e.name for e in IncomeTaxPos.instanceDic.values()],
                    value=manualExpense.taxPosition.name,
                    with_input=True,
                    on_change=update_taxPosition,
                ).tooltip("Verwende Position zur Berechnung der Einkommenssteuer")

                ui.button(
                    icon="edit",
                    on_click=edit_taxPosition,
                ).props(
                    "flat unelevated"
                ).tooltip("Einkommenssteuer-Position bearbeiten")

                ui.button(icon="add", on_click=new_taxPosition).props(
                    "flat unelevated"
                ).tooltip("Neue Einkommenssteuer-Position erstellen")
