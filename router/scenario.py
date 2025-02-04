""" Class for different scenarios in the planning """

from pydantic import BaseModel

class Scenario(BaseModel):
    scenario_id: int
    description: str
    planningYears: int