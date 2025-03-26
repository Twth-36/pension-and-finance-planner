from nicegui import ui
from backend.classes.freeAsset import *
from backend.classes.monthYear import *

# Global container that will hold either the table or the form.
main_container = ui.card().classes("q-pa-md")

def show_overview():
    main_container.clear()
    with main_container:
        with ui.row().classes("items-center q-mb-sm"):
            ui.label("Freie Vermögenswerte").classes("text-h6")
            ui.button(
                on_click=lambda: show_freeAsset_form(),
                icon="add"
            ).props("flat").style("margin-left: auto;")
        
        # Build table from instanceDic
        rows = []
        for freeAsset in FreeAsset.instanceDic.values():
            rows.append({
                "Bezeichnung": freeAsset.name,
                "Person": freeAsset.person.name,
                "Wert": freeAsset.basevalue
            })
        col_defs = [
            {"name": "Bezeichnung", "label": "Bezeichnung", "field": "Bezeichnung"},
            {"name": "Zugehörigkeit", "label": "Zugehörigkeit", "field": "Zugehörigkeit"},
            {"name": "Wert", "label": "Wert", "field": "Wert"}
        ]
        tbl = ui.table(
            columns=col_defs,
            rows=rows,
            row_key="Name"
        ).style("border: none; background-color: transparent;")
        tbl.on('rowClick', lambda r: show_freeAsset_form(person = Person.get_personByName(name=r.args[1]["Name"])))


def show_freeAsset_form(person=None):
    main_container.clear()
    with main_container:
        
        name_input = ui.input(label="Name*", value=person.name if person else "", validation={"Darf nicht leer sein": lambda value: len(value)>0})
        month_input = ui.select(label="Geburtsmonat*", options=list(range(1, 13)), value=person.birth.month if person else None, with_input=True)
        year_input = ui.select(label="Geburtsjahr*", options=list(range(get_currentDate().year-100, get_currentDate().year)), value=person.birth.year if person else None, with_input=True)
       
        with ui.row().classes("q-mt-md"):
            def save_action():
                try:
                    birth_input = MonthYear(month = int(month_input.value), year = int(year_input.value))
                    if person:
                        if person.name != name_input.value: person.update_name(name_input.value)
                        person.birth = birth_input
                    else:
                        Person.create(name=name_input.value, birth=birth_input)
                    show_overview()
                except Exception as e:
                    ui.notify(f"Upps, etwas passte da nicht: \n {e}", color="negative")
                    
            btn_label = "Aktualisieren" if person else "Speichern"
            ui.button(btn_label, on_click=save_action)
            ui.button("Abbrechen", on_click=show_overview).props("outline")

def show_freeAssetTile():
    show_overview()

