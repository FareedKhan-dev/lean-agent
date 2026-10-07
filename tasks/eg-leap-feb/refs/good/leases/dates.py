import calendar
import datetime


def add_months(start, months):
    """The date `months` calendar months after `start`, moved back to the last day of the
    month when the day does not exist there."""
    years, month0 = divmod(start.month - 1 + months, 12)
    year, month = start.year + years, month0 + 1
    return datetime.date(year, month, min(start.day, calendar.monthrange(year, month)[1]))
