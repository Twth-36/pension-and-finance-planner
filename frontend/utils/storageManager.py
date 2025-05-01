# frontend/utils/storageManager.py

from io import BytesIO
from zipfile import ZipFile
from datetime import datetime
import json
from nicegui import ui

from backend.classes.person import Person
from backend.classes.realEstate import RealEstate


def save_all_classes() -> None:
    """
    Erstellt ein ZIP-Archiv mit Person.json und RealEstate.json im Arbeitsspeicher
    und bietet es direkt zum Download im Browser an, ohne eine Datei im Projektordner abzulegen.
    """

    # 1. Daten als JSON-Strings serialisieren
    person_list = [p.model_dump(mode="json") for p in Person.instanceDic.values()]
    realestate_list = [
        r.model_dump(mode="json") for r in RealEstate.instanceDic.values()
    ]
    person_json = json.dumps(person_list, indent=4)
    realestate_json = json.dumps(realestate_list, indent=4)

    # 2. In-Memory-ZIP erzeugen
    buffer = BytesIO()
    with ZipFile(buffer, "w") as zipf:
        zipf.writestr("Person.json", person_json)
        zipf.writestr("RealEstate.json", realestate_json)
    buffer.seek(0)  # zurück an den Anfang des Buffers

    # 3. Timestamp-basierten Dateinamen erstellen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"export_{timestamp}.zip"

    # 4. Download direkt aus Bytes anbieten (kein Schreiben auf Platte)
    ui.download(buffer.getvalue(), filename)


from nicegui import ui
import os, zipfile, json, shutil

# Annahme: Klassen Person und RealEstate sind importiert
# from backend.classes.person import Person
# from backend.classes.realEstate import RealEstate


def handle_upload(event):
    """Callback-Funktion für NiceGUI ui.upload, die das hochgeladene ZIP-Archiv verarbeitet."""
    # Hinweis: 'event' ist vom Typ UploadEventArguments und enthält die hochgeladene Datei.
    temp_zip_path = "uploaded_data.zip"  # Temporärer Pfad für die ZIP-Datei
    temp_extract_dir = (
        "temp_extracted_dir"  # Temporäres Verzeichnis für entpackte Dateien
    )

    try:
        ui.notify("Kommt noch")  # TODO
        return
        # Schritt 1: Hochgeladene ZIP-Datei speichern
        with open(temp_zip_path, "wb") as f:
            # 'event.content' ist ein Dateiobjekt (z.B. BytesIO) – lesen und speichern
            f.write(event.content.read())

        # Schritt 1 (Fortsetzung): ZIP-Archiv entpacken
        with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
            # Entpacken in das temporäre Verzeichnis (Verzeichnis erstellen, falls nicht vorhanden)
            os.makedirs(temp_extract_dir, exist_ok=True)
            zip_ref.extractall(temp_extract_dir)

        # Schritt 1 (Fortsetzung): Pfade der erwarteten JSON-Dateien definieren
        person_json = os.path.join(temp_extract_dir, "Person.json")
        realestate_json = os.path.join(temp_extract_dir, "RealEstate.json")

        # Überprüfen, ob beide Dateien existieren
        if not os.path.isfile(person_json) or not os.path.isfile(realestate_json):
            raise FileNotFoundError(
                "Person.json oder RealEstate.json fehlt im ZIP-Archiv."
            )

        # Schritt 3: JSON-Dateien einlesen
        with open(person_json, "r", encoding="utf-8") as pf:
            person_data_list = json.load(pf)
        with open(realestate_json, "r", encoding="utf-8") as rf:
            realestate_data_list = json.load(rf)

        # Sicherstellen, dass die JSON-Daten Listen sind
        if not isinstance(person_data_list, list) or not isinstance(
            realestate_data_list, list
        ):
            raise ValueError("JSON-Dateien haben nicht das erwartete Listenformat.")

        # Schritt 2: Existierende Objekte löschen
        Person.instanceDic.clear()
        RealEstate.instanceDic.clear()

        # Schritt 3 & 4: Neue Objekte erstellen
        # Zuerst Personen-Objekte erzeugen
        for person_attrs in person_data_list:
            Person.create(**person_attrs)
        # Dann Immobilien-Objekte erzeugen
        for re_attrs in realestate_data_list:
            RealEstate.create(**re_attrs)

        # Schritt 4: Erfolgsnachricht anzeigen
        ui.notify(
            "Daten erfolgreich geladen"
        )  # Erfolgreiche Benachrichtigung für den Benutzer

    except Exception as e:
        # Schritt 4: Fehlerbehandlung – Fehlermeldung im UI anzeigen
        ui.notify(f"Fehler beim Laden: {e}", type="error")

    finally:
        # Schritt 5: Aufräumen der temporären Dateien
        try:
            if os.path.exists(temp_zip_path):
                os.remove(temp_zip_path)  # Lösche die gespeicherte ZIP-Datei
            if os.path.isdir(temp_extract_dir):
                shutil.rmtree(
                    temp_extract_dir
                )  # Lösche das entpackte Verzeichnis und dessen Inhalt
        except Exception as cleanup_error:
            # Im Fehlerfall beim Aufräumen kann optional eine Log-Meldung erfolgen.
            print(
                f"Warnung: Temporäre Dateien konnten nicht vollständig gelöscht werden: {cleanup_error}"
            )
