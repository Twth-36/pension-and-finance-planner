from nicegui import ui

from backend.classes.taxes import Taxes
from backend.tax.taxproperties import Canton, Taxation


def show_taxesOverview(taxes_card):
    taxes_card.clear()
    with taxes_card:
        # Header
        with ui.row().classes("justify-center items-center"):
            ui.label("Steuergrundlagen").classes("text-h6")

        with ui.column():

            # **Canton**
            def update_canton(change):
                try:
                    Taxes.canton = Canton(change.value)
                    Taxes.place = None
                    show_taxesOverview(taxes_card)
                    ui.notify("Änderung aktualisiert", color="positive")
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:\n{e}", color="negative")

            ui.select(
                label="Wohnkanton*",
                options=[c.value for c in Canton],
                value=Taxes.canton.value if Taxes.canton else None,
                on_change=update_canton,
            ).classes("w-full")

            # **Taxation**
            def update_taxation(change):
                try:
                    Taxes.taxation = Taxation(change.value)
                    ui.notify("Änderung aktualisiert", color="positive")
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:\n{e}", color="negative")

            ui.select(
                label="Besteuerung",
                options=[m.value for m in Taxation],
                value=Taxes.taxation.value,
                on_change=update_taxation,
            ).tooltip(
                "Bei einzelner Besteuerung werden sämtliche Personen individuell zum Alleinstehenden-Satz besteuert."
                "Positionen ohne Personenzuweisung werden je hälftig berücksichtigt. Andernfalls werden die Steuern kumuliert zum verheirateten-Satz berechnet."
            )

            # Place
            def update_place(new_place: str):
                try:
                    Taxes.place = new_place
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht: {e}", color="negative")
                ui.notify("Änderung aktualisiert", color="positive")

            place_input = ui.input(label="Wohnort", value=Taxes.place or "").tooltip(
                "Wohnort für Besteuerung"
            )
            place_input.on("blur", lambda: update_place(place_input.value))
