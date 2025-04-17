from nicegui import ui
from backend.classes.credit import Credit
from backend.classes.freeAsset import FreeAsset
from backend.classes.pensionFund import PensionFund
from backend.classes.pillar3a import Pillar3a
from backend.classes.realEstate import RealEstate


def show_wealthOverview():
    pension_total = sum(p.baseValue or 0 for p in PensionFund.instanceDic.values())
    pillar3a_total = sum(p.baseValue or 0 for p in Pillar3a.instanceDic.values())
    free_asset_total = sum(f.baseValue or 0 for f in FreeAsset.instanceDic.values())
    real_estate_total = sum(r.baseValue or 0 for r in RealEstate.instanceDic.values())

    for c in Credit.instanceDic.values():
        if c.realEstate is None:
            free_asset_total -= c.baseValue or 0
        else:
            real_estate_total -= c.baseValue or 0

    data = [
        {"name": "Pensionskassen", "value": pension_total},
        {"name": "Säule 3a", "value": pillar3a_total},
        {"name": "Freie Vermögenswerte", "value": free_asset_total},
        {"name": "Liegenschaften", "value": real_estate_total},
    ]

    ui.echart(
        {
            "series": [
                {
                    "type": "pie",
                    "radius": ["35%", "70%"],
                    "avoidLabelOverlap": False,
                    "label": {
                        "show": True,
                        "position": "outside",
                        "formatter": "{b}",
                        "fontSize": 18,
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
