"""Class for simple date format month, year"""

from pydantic import BaseModel
from datetime import datetime


class MonthYear(BaseModel):
    month: int
    year: int

    def dateToString(self) -> "str":
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


def validate_dateFormat(input: str) -> bool:
    if not (
        len(input) == 7
        and input[2] == "."
        and input[:2].isdigit()
        and input[3:].isdigit()
    ):
        return False

    month = int(input[:2])
    year = int(input[3:])

    return 1 <= month <= 12 and year > 0


def stringToDate(input: str) -> "MonthYear":
    if not validate_dateFormat(input):
        raise ValueError(f"{input} has not format MM.YYYY")

    month = int(input[:2])
    year = int(input[3:])

    return MonthYear(month=month, year=year)
