from nicegui import ui
from backend.classes.credit import Credit
from backend.classes.freeAsset import FreeAsset
from backend.classes.pensionFund import PensionFund
from backend.classes.pillar3a import Pillar3a
from backend.classes.pillar3aPolice import Pillar3aPolice
from backend.classes.pillar3bPolice import Pillar3bPolice
from backend.classes.realEstate import RealEstate
from backend.classes.vestedBenefit import VestedBenefit


def show_wealthOverviewChart():
    free_asset_total = sum(f.baseValue or 0 for f in FreeAsset.instanceDic.values())
    real_estate_total = sum(r.baseValue or 0 for r in RealEstate.instanceDic.values())

    for c in Credit.instanceDic.values():
        if c.realEstate is None:
            free_asset_total -= c.baseValue or 0
        else:
            real_estate_total -= c.baseValue or 0

    pension_total = sum(p.baseValue or 0 for p in PensionFund.instanceDic.values())
    pension_total += sum(p.baseValue or 0 for p in VestedBenefit.instanceDic.values())
    pension_total += sum(p.baseValue or 0 for p in Pillar3a.instanceDic.values())
    pension_total += sum(p.baseValue or 0 for p in Pillar3aPolice.instanceDic.values())
    pension_total += sum(p.baseValue or 0 for p in Pillar3bPolice.instanceDic.values())

    data = [
        {"name": "Freie Vermögenswerte", "value": free_asset_total},
        {"name": "Liegenschaften", "value": real_estate_total},
        {"name": "Vorsorgegelder", "value": pension_total},
    ]

    ui.echart(
        {
            "legend": {"left": "5%", "orient": "vertical"},
            "series": [
                {
                    "type": "pie",
                    "radius": ["35%", "70%"],
                    "avoidLabelOverlap": False,
                    "label": {
                        "show": True,
                        "position": "outside",
                        "formatter": "{d}%",
                        "fontSize": 14,
                    },
                    "labelLine": {"show": True, "length": 20, "length2": 20},
                    "emphasis": {
                        "label": {
                            "show": True,
                            "fontWeight": "bold",
                            "formatter": "{b}: {d}%",
                        }
                    },
                    "data": data,
                }
            ],
        }
    )
