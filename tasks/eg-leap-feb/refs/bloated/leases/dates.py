import calendar
import datetime
from dataclasses import dataclass
from enum import Enum


class EndOfMonth(Enum):
    CLAMP = "clamp"          # 31 Jan + 1 month -> 28 or 29 Feb
    OVERFLOW = "overflow"    # 31 Jan + 1 month -> 3 or 2 Mar
    STRICT = "strict"        # 31 Jan + 1 month -> error


class LeaseCalendar:
    def __init__(self, policy=EndOfMonth.CLAMP):
        self.policy = policy

    def days_in_month(self, year, month):
        return calendar.monthrange(year, month)[1]

    def shift(self, start, months):
        years, month0 = divmod(start.month - 1 + months, 12)
        year, month = start.year + years, month0 + 1
        last = self.days_in_month(year, month)
        if start.day <= last:
            return datetime.date(year, month, start.day)
        if self.policy is EndOfMonth.CLAMP:
            return datetime.date(year, month, last)
        if self.policy is EndOfMonth.OVERFLOW:
            return datetime.date(year, month, last) + datetime.timedelta(days=start.day - last)
        raise ValueError(f"{start} plus {months} months does not exist")


@dataclass(frozen=True)
class MonthDelta:
    months: int
    policy: EndOfMonth = EndOfMonth.CLAMP

    def __radd__(self, start):
        return LeaseCalendar(self.policy).shift(start, self.months)


def add_months(start, months):
    """The date `months` calendar months after `start`, moved back to the last day of the
    month when the day does not exist there."""
    return start + MonthDelta(months)
