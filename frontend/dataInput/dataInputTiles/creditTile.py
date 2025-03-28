from nicegui import ui
from backend.classes.credit import *
from backend.classes.monthYear import *
from frontend.utils import *


def show_creditTile():
    # Create a card container for credits
    credit_card = ui.card().classes("q-pa-md border hover:!shadow-2xl")

    def show_overview():
        credit_card.clear()
        with credit_card:
            # Header
            with ui.row().classes("justify-center items-center"):
                ui.label("Kredite / Hypotheken").classes("text-h6")
            # Table of Credit entries
            with ui.column():
                rows = [
                    {
                        "Name": c.name,
                        "Zugehörigkeit": (c.person.name if c.person else ""),
                        "Betrag": c.baseValue,
                    }
                    for c in Credit.instanceDic.values()
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
                # Action buttons
                with ui.row().classes("items-center q-mb-sm"):
                    ui.button(icon="add", on_click=lambda: show_credit_form()).props(
                        "flat unelevated"
                    )

                    def edit_action():
                        if len(tbl.selected) != 1:
                            ui.notify("Wähle eine Zeile aus.")
                        else:
                            sel_name = tbl.selected[0]["Name"]
                            credit = Credit.get_itemByName(name=sel_name)
                            show_credit_form(credit=credit)

                    ui.button(icon="edit", on_click=edit_action).props(
                        "flat unelevated"
                    )

                    async def del_action():
                        if len(tbl.selected) == 0:
                            ui.notify("Wähle mindestens eine Zeile aus.")
                        else:
                            if await show_confDialog():
                                for item in tbl.selected:
                                    Credit.get_itemByName(item["Name"]).delete_item()
                                ui.notify("Gelöscht", color="positive")
                                show_overview()  # simply refresh list

                    ui.button(icon="delete", on_click=del_action).props(
                        "flat unelevated"
                    )

                    ui.button(icon="refresh", on_click=show_overview).props(
                        "flat unelevated"
                    )

        def show_credit_form(credit=None):
            credit_card.clear()
            with credit_card:
                # Input fields for credit data
                name_input = ui.input(
                    label="Name*",
                    value=(credit.name if credit else ""),
                    validation={"Darf nicht leer sein": lambda v: len(v) > 0},
                ).props("autofocus")
                person_prefill = (
                    credit.person.name if (credit and credit.person) else None
                )
                person_input = ui.select(
                    label="Zugehörigkeit",
                    options=[p.name for p in Person.instanceDic.values()],
                    value=person_prefill,
                    with_input=True,
                )
                base_val_input = ui.number(
                    label="Wert",
                    value=(credit.baseValue if credit else None),
                    validation={
                        "Muss grösser oder gleich 0 sein": lambda v: v is None or v >= 0
                    },
                )
                interest_input = ui.number(
                    label="Zinssatz",
                    value=(credit.baseInterestRate if credit else None),
                    format="%.1f",
                ).props("suffix=%")

                endDate_prefill = None
                if credit:
                    if credit.endDate:
                        endDate_prefill = credit.endDate.dateToString()
                endDate_input = ui.input(
                    label="Ablaufmonat",
                    placeholder="MM.JJJJ",
                    validation={
                        "Format nicht korrekt": lambda v: validate_dateFormat(v)
                    },
                    value=endDate_prefill,
                )

                with ui.row():

                    def save_action():
                        try:
                            if credit:  # Update existing
                                if credit.name != name_input.value:
                                    credit.update_name(name_input.value)
                                credit.person = (
                                    Person.get_itemByName(person_input.value)
                                    if person_input.value
                                    else None
                                )
                                if base_val_input.value:
                                    credit.baseValue = base_val_input.value
                                if interest_input.value:
                                    credit.interestRate = interest_input.value
                                if endDate_input.value:
                                    credit.endDate = stringToDate(endDate_input.value)

                            else:  # Create new credit
                                params = {"name": name_input.value}
                                if person_input.value not in [None, ""]:
                                    params["person"] = Person.get_itemByName(
                                        person_input.value
                                    )
                                if base_val_input.value:
                                    params["baseValue"] = base_val_input.value
                                if interest_input.value:
                                    params["baseInterestRate"] = interest_input.value
                                if endDate_input.value:
                                    params["endDate"] = stringToDate(
                                        endDate_input.value
                                    )
                                Credit.create(**params)
                            show_overview()
                        except Exception as e:
                            ui.notify(
                                f"Upps, etwas passte da nicht:\n{e}", color="negative"
                            )

                    btn_label = "Aktualisieren" if credit else "Speichern"
                    ui.button(btn_label, on_click=save_action)
                    ui.button("Abbrechen", on_click=show_overview).props("outline")

    # Initialize by showing the overview
    show_overview()
    return credit_card
