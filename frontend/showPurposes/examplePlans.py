import json
from pathlib import Path
from frontend.utils.confDialog import show_confDialog
from frontend.utils.storageManager import load_data_dict
from nicegui import ui


async def handle_load_example(example_filename: str):
    if not await show_confDialog(
        f"Daten aus {example_filename} laden? Die aktuellen Daten werden überschrieben!"
    ):
        return
    path = Path(__file__).parent / example_filename
    if not path.exists():
        ui.notify(f"Datei {example_filename!r} nicht gefunden.", color="negative")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    await load_data_dict(data)
