from nicegui import ui

from backend.classes.freeAsset import FreeAsset
from backend.classes.person import Person


def show_freeAssetForm(freeAsset_card, freeAsset=None):
    freeAsset_card.clear()
    with freeAsset_card:
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
                            params["person"] = Person.get_itemByName(person_input.value)
                        if base_value_input.value not in [None, ""]:
                            params["baseValue"] = base_value_input.value
                        FreeAsset.create(**params)
                    show_freeAssetOverview(freeAsset_card)  # return to overview
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:\n{e}", color="negative")

            ui.button("Speichern", on_click=save_action)
            # Use local import to avoid circular dependency
            from .freeAssetOverview import show_freeAssetOverview

            ui.button(
                "Schliessen",
                on_click=lambda: show_freeAssetOverview(freeAsset_card),
            ).props("outline")
            ui.button(
                icon="refresh",
                on_click=lambda: show_freeAssetForm(freeAsset_card, freeAsset),
            ).props("flat unelevated")
