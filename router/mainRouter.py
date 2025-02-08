""" router for all general communication via API"""

#starting router
from fastapi import APIRouter
from showPurposes.examplePlans import *

router = APIRouter(prefix="/mainRouter", tags=["mainRouter"])


# Returns all Persons
@router.get("/load-examplePlan/{example_name}")
def get_examplePlan(example_name: str):
    match example_name:
        case "Verheiratetes Paar":
            examplePlanMarried()
            return {example_name: "geladen"}
        case "Paar in Konkubinat":
            return {example_name: "noch nicht erstellt"}
        case "Alleinstehend":
            return {example_name: "noch nicht erstellt"}
        case _:
            return {example_name: "nicht vorhanden"}
