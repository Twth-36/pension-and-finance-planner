""" Class for simple date format month, year """

from pydantic import BaseModel
from datetime import datetime

class MonthYear(BaseModel):
    month: int
    year: int

    def get_dateAsString(self) -> "str":
        return str(self.month).zfill(2) + "." + str(self.year)

# Get the last month of the last year
def get_lastYearLastMonth() -> "MonthYear":
    lastmonth = 12
    lastyear = datetime.now().year - 1
    
    return MonthYear(month=lastmonth, year=lastyear)

def get_currentDate() -> "MonthYear":
    month = datetime.now().month
    year = datetime.now().year

    return MonthYear(month=month, year=year)




