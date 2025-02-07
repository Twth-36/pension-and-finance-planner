""" router for all general communication via API"""

#starting router
from fastapi import APIRouter

router = APIRouter(prefix="/mainRouter", tags=["mainRouter"])

# Returns all Persons
@router.get("/load-examplePlan/{example_name}")
def get_examplePlan(example_name: str):
    match example_name:
        case "Verheirates Paar":
            return {example_name: "geladen"}
        case _:
            return {example_name: "noch nicht erstellt"}