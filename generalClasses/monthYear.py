""" Class for simple date format month, year """

from pydantic import BaseModel

class MonthYear(BaseModel):
    month: int
    year: int
