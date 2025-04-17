from nicegui import ui

from backend.classes.taxes import Taxes
from backend.tax.taxproperties import Canton, Taxation


def show_taxesOverview(taxes_card):
    taxes_card.clear()
    with taxes_card:
        # Header
        with ui.row().classes("justify-center items-center"):
            ui.label("Steuergrundlagen").classes("text-h6")
            ui.label(f"Basisjahr: {Taxes.baseYearTaxCalc}").classes(
                "italic text-sm text-gray-600"
            )

        with ui.column():

            # **Canton**
            def update_canton(change):
                try:
                    Taxes.update_canton(new_canton=Canton(change.value))
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

            # **Place**
            def update_place(change):
                try:
                    Taxes.update_place(new_place=change.value)
                    show_taxesOverview(taxes_card)
                    ui.notify("Änderung aktualisiert", color="positive")
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:\n{e}", color="negative")

            place_options = []
            if Taxes.canton:
                try:
                    place_options = Taxes.canton.get_placeNames()
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:{e}", color="negative")

            place_prefill = None
            if Taxes.place:
                place_prefill = Taxes.place
            ui.select(
                label="Wohnort*",
                options=place_options,
                value=place_prefill,
                on_change=update_place,
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

            # **taxRate Canton

            # TODO

            # **taxRateCom
            # **Taxation**
            def update_taxRateCom(new_taxRate: float):
                try:
                    Taxes.taxRateCom = new_taxRate
                    ui.notify("Änderung aktualisiert", color="positive")
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht:\n{e}", color="negative")

            taxRateCom_input = (
                ui.number(
                    label="Steuersatz Gemeinde",
                    value=(Taxes.taxRateCom if Taxes.taxRateCom else None),
                    format="%.2f",
                )
                .props("suffix=%")
                .tooltip("Steuersatz zur Berechnung der Liegenschaftssteuer.")
            )
            taxRateCom_input.on(
                "blur", lambda: update_taxRateCom(new_taxRate=taxRateCom_input.value)
            )
