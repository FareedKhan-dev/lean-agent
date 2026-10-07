import datetime

DAILY_FINE_PENCE = 20
LOAN_DAYS = 14


class FineStrategy:
    """How a fine is worked out from the number of days a book is late."""

    def fine_for(self, days_late):
        raise NotImplementedError


class DailyFine(FineStrategy):
    def __init__(self, pence_per_day=DAILY_FINE_PENCE):
        self.pence_per_day = pence_per_day

    def fine_for(self, days_late):
        return days_late * self.pence_per_day


def make_strategy(kind="daily"):
    if kind == "daily":
        return DailyFine()
    raise ValueError(f"unknown fine strategy {kind!r}")


def due_date(borrowed):
    return borrowed + datetime.timedelta(days=LOAN_DAYS)


def days_late(borrowed, returned):
    """Whole days after the due date on which the book was still out."""
    return max(0, (returned - due_date(borrowed)).days + 1)


def fine(borrowed, returned, strategy=None):
    return (strategy or make_strategy()).fine_for(days_late(borrowed, returned))
