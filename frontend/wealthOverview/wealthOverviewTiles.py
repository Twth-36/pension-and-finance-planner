from nicegui import ui
from backend.classes.credit import Credit
from backend.classes.freeAsset import FreeAsset
from backend.classes.pensionFund import PensionFund
from backend.classes.pillar3a import Pillar3a
from backend.classes.pillar3aPolice import Pillar3aPolice
from backend.classes.pillar3bPolice import Pillar3bPolice
from backend.classes.realEstate import RealEstate
from backend.classes.vestedBenefit import VestedBenefit
from frontend.utils.format import formatswiss


def show_wealthOverviewTiles():
    # calculate raw values
    freeAsset_total = sum(f.baseValue or 0 for f in FreeAsset.instanceDic.values())
    realEstate_total = sum(r.baseValue or 0 for r in RealEstate.instanceDic.values())

    # aggregate credits and mortgages as positive numbers
    other_credits = sum(
        abs(c.baseValue or 0)
        for c in Credit.instanceDic.values()
        if c.realEstate is None
    )
    mortgages = sum(
        abs(c.baseValue or 0)
        for c in Credit.instanceDic.values()
        if c.realEstate is not None
    )

    # compute net values
    free_net = freeAsset_total - other_credits
    realestate_net = realEstate_total - mortgages
    pension_total = sum(p.baseValue or 0 for p in PensionFund.instanceDic.values())
    pension_total += sum(p.baseValue or 0 for p in VestedBenefit.instanceDic.values())
    pension_total += sum(p.baseValue or 0 for p in Pillar3a.instanceDic.values())
    pension_total += sum(p.baseValue or 0 for p in Pillar3aPolice.instanceDic.values())
    pension_total += sum(p.baseValue or 0 for p in Pillar3bPolice.instanceDic.values())

    # grand totals
    grand_total = free_net + realestate_net + pension_total
    without_realestate_tot = grand_total - realestate_net

    # display cards with improved typography
    with ui.row().classes("q-gutter-md"):
        # Free Assets Card
        with ui.card().classes("q-pa-md border hover:!shadow-2xl"):
            ui.label("Freie Vermögenswerte").classes("text-h6")
            with ui.grid(columns=2).classes("items-center"):
                ui.label("Gesamtwert:").classes("text-body1 font-medium")
                ui.label(formatswiss(freeAsset_total)).classes(
                    "text-body1 font-semibold text-right"
                )

                ui.label("Kredite:").classes("text-body1 font-medium")
                ui.label(formatswiss(other_credits)).classes(
                    "text-body1 font-semibold text-right"
                )

                ui.label("Netto:").classes("text-body1 font-medium")
                ui.label(formatswiss(free_net)).classes(
                    "text-body1 font-semibold text-right"
                )

                ui.label("Vermögensanteil:").classes("text-body2")
                ui.label(
                    f"{formatswiss(free_net/grand_total*100, decimals=1)}%"
                ).classes("text-body2 font-medium text-right")

                ui.label("Anteil ohne Liegenschaften:").classes("text-body2")
                ui.label(
                    f"{formatswiss(free_net/without_realestate_tot*100, decimals=1)}%"
                ).classes("text-body2 font-medium text-right")

        # Pensions Card
        with ui.card().classes("q-pa-md border hover:!shadow-2xl"):
            ui.label("Vorsorgegelder").classes("text-h6")
            with ui.grid(columns=2).classes("items-center"):
                ui.label("Gesamtwert:").classes("text-body1 font-medium")
                ui.label(formatswiss(pension_total)).classes(
                    "text-body1 font-semibold text-right"
                )

                ui.label("Vermögensanteil:").classes("text-body2")
                ui.label(
                    f"{formatswiss(pension_total/grand_total*100, decimals=1)}%"
                ).classes("text-body2 font-medium text-right")

                ui.label("Anteil ohne Liegenschaften:").classes("text-body2")
                ui.label(
                    f"{formatswiss(pension_total/without_realestate_tot*100, decimals=1)}%"
                ).classes("text-body2 font-medium text-right")

        # Real Estate Card
        with ui.card().classes("q-pa-md border hover:!shadow-2xl"):
            ui.label("Liegenschaften").classes("text-h6")
            with ui.grid(columns=2).classes("items-center"):
                ui.label("Gesamtwert:").classes("text-body1 font-medium")
                ui.label(formatswiss(realEstate_total)).classes(
                    "text-body1 font-semibold text-right"
                )

                ui.label("Hypotheken:").classes("text-body1 font-medium")
                ui.label(formatswiss(mortgages)).classes(
                    "text-body1 font-semibold text-right"
                )

                ui.label("Netto:").classes("text-body1 font-medium")
                ui.label(formatswiss(realestate_net)).classes(
                    "text-body1 font-semibold text-right"
                )

                ui.label("Vermögensanteil:").classes("text-body2")
                ui.label(
                    f"{formatswiss(realestate_net/grand_total*100, decimals=1)}%"
                ).classes("text-body2 font-medium text-right")
