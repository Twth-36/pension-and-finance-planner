from nicegui import ui

from frontend.wealthOverview.wealthOverviewChart import show_wealthOverviewChart
from frontend.wealthOverview.wealthOverviewTiles import show_wealthOverviewTiles


def show_wealthOverview(main_content):
    main_content.clear()
    with main_content:

        with ui.column():
            show_wealthOverviewChart()
            show_wealthOverviewTiles()
