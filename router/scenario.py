""" Class for different scenarios in the planning """

from pydantic import BaseModel
from fastapi import APIRouter
from typing import Optional
from generalClasses.monthYear import *


class Scenario(BaseModel):
    scenario_id: Optional[int] = 0
    description: str

# Planninghorizon for all scenarios identical
baseDate = get_lastYearLastMonth
endDate = get_lastYearLastMonth

#Dictionary for managing all scenario position
scenarioDic = {}

#starting router
router = APIRouter()

# Returs basedate
@router.post("/scenario/get-baseDate/")
def get_baseDate():
    return baseDate

#creating a new scenario-object
@router.post("/scenario/create-scenario/{scenario_id}")
def create_scenario(scenario_id: int, scenario: Scenario):
    if scenario_id in scenarioDic:
        return {"Error": "scenario_id already used"}
    
    scenarioDic[scenario_id] = scenario
    return scenarioDic[scenario_id]

# Changes on existing scenario-object
@router.put("/scenario/update-scenario/{scenario_id}")
def update_scenario(scenario_id: int, scenario: Scenario):
    if scenario_id not in scenarioDic:
        return {"Error": "scenario_id not found"}
    
    scenarioDic[scenario_id].update(scenario)
    return scenarioDic[scenario_id]

# Deleting an existing scenario object
@router.delete("/scenario/delete-scenario/{scenario_id}")
def delete_scenario(scenario_id: int):
    if scenario_id not in scenarioDic:
        return {"Error": "scenario_id not found"}
    
    del scenarioDic[scenario_id]
    return {"Success": "Scenario deleted"}

# Returns scenario position by id
@router.get("/scenario/get-scenario/{scenario_id}")
def get_scenario(scenario_id: int):
    if scenario_id not in scenarioDic:
        return {"Error": "scenario_id not found"}
    return scenarioDic[scenario_id]

# Returns all Scenarios
@router.get("/scenario/get-allscenarios/")
def get_allscenarios():
    return scenarioDic


# Generate Base scenario base-value inputs which get used by all scenarios
scenarioDic[0] = Scenario(scenario_id=0, description="Base Scenario", baseDate=get_lastYearLastMonth(), endDate=get_lastYearLastMonth())
