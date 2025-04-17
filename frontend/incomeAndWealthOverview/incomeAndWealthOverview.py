from nicegui import ui

from frontend.incomeAndWealthOverview.incomeOverview import show_incomeOverview
from frontend.incomeAndWealthOverview.wealthOverview import show_wealthOverview


def show_incomeAndWealthOverview(main_content):
    main_content.clear()
    with main_content:
        ui.label("Einkommensübersicht").classes("text-h6 font-bold q-mt-md")
        with ui.row():
            show_incomeOverview()

        ui.label("Vermögensübersicht").classes("text-h6 font-bold q-mt-md")

        with ui.row().classes("w-full justify-center"):
            show_wealthOverview()
