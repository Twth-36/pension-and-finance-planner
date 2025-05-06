"""Class for simple date format month, year"""

from typing import List
from pydantic import BaseModel
from datetime import datetime


class MonthYear(BaseModel):
    month: int
    year: int

    # Get the last month of the last year
    @classmethod
    def get_lastYearLastMonth(cls) -> "MonthYear":
        lastmonth = 12
        lastyear = datetime.now().year - 1

        return MonthYear(month=lastmonth, year=lastyear)

    @classmethod
    def get_currentDate(cls) -> "MonthYear":
        month = datetime.now().month
        year = datetime.now().year

        return MonthYear(month=month, year=year)

    @classmethod
    def validate_dateFormat(cls, input: str) -> bool:
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

    @classmethod
    def stringToDate(cls, input: str) -> "MonthYear":
        if not MonthYear.validate_dateFormat(input):
            raise ValueError(f"{input} has not format MM.YYYY")

        month = int(input[:2])
        year = int(input[3:])

        return MonthYear(month=month, year=year)

    def dateToString(self) -> "str":
        return str(self.month).zfill(2) + "." + str(self.year)

    # string of the date without "." since it can get wrongly interpreted
    def dateToID(self) -> "str":
        return str(self.month).zfill(2) + str(self.year)

    def nextMonth(self, n: int = 1) -> "MonthYear":
        # returns n-next (or previous if n <0 month)
        total_mnths = self.year * 12 + (self.month - 1) + n
        new_year = total_mnths // 12  # floor division
        new_month = (total_mnths % 12) + 1
        return MonthYear(month=new_month, year=new_year)

    @classmethod
    def create_range(
        cls, startDate: "MonthYear", endDate: "MonthYear"
    ) -> List["MonthYear"]:

        # Return a list of MonthYear from startDate up to endDate inclusive.

        if (startDate.year, startDate.month) > (endDate.year, endDate.month):
            raise ValueError("startDate must be before or equal to endDate")

        result: List[MonthYear] = []
        current = startDate
        # keep going until we pass endDate
        while (current.year, current.month) <= (endDate.year, endDate.month):
            result.append(current)
            current = current.nextMonth()
        return result

    @classmethod
    def months_diff(cls, startDate: "MonthYear", endDate: "MonthYear"):
        return (endDate.year - startDate.year) * 12 + (endDate.month - startDate.month)
