import datetime

DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def add_months(start, months):
    """The date `months` calendar months after `start`, moved back to the last day of the
    month when the day does not exist there."""
    total = start.month - 1 + months
    year, month = start.year + total // 12, total % 12 + 1
    last = 29 if month == 2 and year % 4 == 0 else DAYS[month - 1]
    return datetime.date(year, month, min(start.day, last))
