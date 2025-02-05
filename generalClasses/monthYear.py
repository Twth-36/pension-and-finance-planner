""" Class for simple date format month, year """

from pydantic import BaseModel
from datetime import datetime

class MonthYear(BaseModel):
    month: int
    year: int

# Get current Year
def get_lastYearLastMonth():
    lastmonth = 12
    lastyear = datetime.now().year - 1
    
    return MonthYear(month=lastmonth, year=lastyear)


