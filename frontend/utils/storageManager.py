# frontend/utils/storageManager.py

from datetime import datetime
import json
from nicegui import ui
from pydantic import TypeAdapter, parse_obj_as

from backend.classes.cashflow import Cashflow
from backend.classes.credit import Credit
from backend.classes.expense import Expense
from backend.classes.freeAsset import FreeAsset
from backend.classes.income import Income
from backend.classes.incomeTaxPos import IncomeTaxPos
from backend.classes.manualExpense import ManualExpense
from backend.classes.manualIncome import ManualIncome
from backend.classes.manualIncomeTaxPos import ManualIncomeTaxPos
from backend.classes.pensionFund import PensionFund
from backend.classes.person import Person
from backend.classes.pillar3a import Pillar3a
from backend.classes.pillar3aPolice import Pillar3aPolice
from backend.classes.pillar3bPolice import Pillar3bPolice
from backend.classes.realEstate import RealEstate
from backend.classes.scenario import Scenario
from backend.classes.taxes import Taxes
from backend.classes.vestedBenefit import VestedBenefit
from backend.tax.taxproperties import Canton, Taxation
from backend.utils.monthYear import MonthYear
from frontend.utils.confDialog import show_confDialog

# order is crucial no class may have an object-attribute of a later class
classes_with_instanceDic = [
    Person,
    Scenario,
    IncomeTaxPos,
    ManualIncomeTaxPos,
    Expense,
    Income,
    ManualExpense,
    ManualIncome,
    Cashflow,
    RealEstate,
    Credit,
    FreeAsset,
    PensionFund,
    Pillar3a,
    Pillar3aPolice,
    Pillar3bPolice,
    VestedBenefit,
]


def save_all_classes() -> None:

    data_for_json = {}

    for cls in classes_with_instanceDic:
        data_for_json[cls.__name__ + "_objects"] = [
            obj.model_dump(mode="json") for obj in cls.instanceDic.values()
        ]

    # classVars of Classes with additional information which needs to be saved
    """Expense"""
    data_for_json["expense_classVars"] = {
        "cashflowPos": Expense.cashflowPos.model_dump(mode="json")
    }

    """ FreeAssets"""
    data_for_json["freeAsset_classVars"] = {
        "liqRes": FreeAsset.liqRes,
        "returnRateInvestCap": FreeAsset.returnRateInvestCap,
        "returnIncome": (
            FreeAsset.returnIncome.model_dump(mode="json")
            if FreeAsset.returnIncome
            else None
        ),
    }

    """Income"""
    data_for_json["income_classVars"] = {
        "cashflowPos": Income.cashflowPos.model_dump(mode="json")
    }

    """Scneario"""
    data_for_json["scenario_classVars"] = {
        "baseDate": Scenario.baseDate.model_dump(mode="json"),
        "endDate": Scenario.endDate.model_dump(mode="json"),
    }

    """Taxes"""
    data_for_json["taxes_classVars"] = {
        "canton": Taxes.canton.value,
        "place": Taxes.place,
        "taxation": Taxes.taxation.value,
        "childrenCnt": Taxes.childrenCnt,
        "incTaxExpense": Taxes.incTaxExpense.model_dump(mode="json"),
        "wlthTaxExpense": Taxes.wlthTaxExpense.model_dump(mode="json"),
        "capPayoutTaxExpense": Taxes.capPayoutTaxExpense.model_dump(mode="json"),
    }
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"export_{timestamp}.json"

    # create JSON with nice format (4)
    json_str = json.dumps(data_for_json, indent=4)

    # download JSON-File
    ui.download(json_str.encode("utf-8"), filename)


async def load_data_dict(data: dict) -> None:

    try:

        n = ui.notification("Lade Daten…")
        # 1) delete old instances
        for cls in classes_with_instanceDic:
            cls.instanceDic.clear()

        # 3) recreate objects (order of classes_with_instanceDic is crucial)
        for cls in classes_with_instanceDic:
            key = cls.__name__ + "_objects"
            objects = data.get(key, [])
            if not isinstance(objects, list):
                raise ValueError(f"{key} is not a list")
            for attrs in objects:
                cls.create(**attrs)

        # 4) manually assign classVars
        """Expense"""
        cv = data.get("expense_classVars", {})
        if cv.get("cashflowPos"):
            Expense.cashflowPos = Cashflow.get_itemByName(cv.get("cashflowPos")["name"])

        """FreeAsset"""
        cv = data.get("freeAsset_classVars", {})
        FreeAsset.liqRes = cv.get("liqRes", 0)
        FreeAsset.returnRateInvestCap = cv.get("returnRateInvestCap", 0)
        if cv.get("returnIncome"):
            FreeAsset.returnIncome = Income.get_itemByName(
                cv.get("returnIncome")["name"]
            )

        """Income"""
        cv = data.get("income_classVars", {})
        if cv.get("cashflowPos"):
            Income.cashflowPos = Cashflow.get_itemByName(cv.get("cashflowPos")["name"])

        """Scenario"""
        cv = data.get("scenario_classVars", {})
        # baseDate: Dict → MonthYear
        base_date_data = cv.get("baseDate")
        if isinstance(base_date_data, dict):
            Scenario.baseDate = MonthYear.model_validate(base_date_data)
        elif isinstance(base_date_data, MonthYear):
            Scenario.baseDate = base_date_data
        else:
            Scenario.baseDate = None

        # endDate: Dict → MonthYear
        end_date_data = cv.get("endDate")
        if isinstance(end_date_data, dict):
            Scenario.endDate = MonthYear.model_validate(end_date_data)
        elif isinstance(end_date_data, MonthYear):
            Scenario.endDate = end_date_data
        else:
            Scenario.endDate = None

        # Taxes
        cv = data.get("taxes_classVars", {})
        Taxes.canton = TypeAdapter(Canton).validate_python(cv.get("canton"))
        Taxes.place = cv.get("place")
        Taxes.taxation = TypeAdapter(Taxation).validate_python(cv.get("taxation"))
        Taxes.childrenCnt = cv.get("childrenCnt", 0)
        if cv.get("incTaxExpense"):
            Taxes.incTaxExpense = Expense.get_itemByName(cv["incTaxExpense"]["name"])
        if cv.get("wlthTaxExpense"):
            Taxes.wlthTaxExpense = Expense.get_itemByName(cv["wlthTaxExpense"]["name"])
        if cv.get("capPayoutTaxExpense"):
            Taxes.capPayoutTaxExpense = Expense.get_itemByName(
                cv["capPayoutTaxExpense"]["name"]
            )

        n.dismiss()
        ui.notify(
            "Daten erfolgreich geladen. Denke daran die aktuelle Seite allenfalls erneut zu laden!",
            color="positive",
        )

    except Exception as e:
        n.dismiss()
        ui.notify(f"Fehler beim Laden: {e}", type="error")


async def handle_upload(event):
    """Load JSON-File and build all data new up"""

    if await show_confDialog("Bist du sicher?  \n Alle Daten werden überschrieben!"):

        # JSON einlesen
        content = event.content.read()
        data = json.loads(content)

        if not isinstance(data, dict):
            raise ValueError("Erwartetes JSON-Objekt, aber got " + type(data).__name__)

        await load_data_dict(data)

    event.sender.reset()
