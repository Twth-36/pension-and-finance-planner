""" Class for simple date format month, year """

from pydantic import BaseModel

class MonthYear(BaseModel):
    month: int
    year: int

    def __init__(self, month: int, year: int):
        self.month = month
        self.year = year