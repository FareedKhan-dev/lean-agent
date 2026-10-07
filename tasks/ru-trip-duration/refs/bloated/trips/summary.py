from dataclasses import dataclass


@dataclass(frozen=True)
class Duration:
    """A length of time, formatted for the trip list."""

    seconds: float

    @property
    def total_minutes(self):
        return round(self.seconds / 60)

    @property
    def parts(self):
        return divmod(self.total_minutes, 60)

    def format(self):
        hours, minutes = self.parts
        if not hours:
            return f"{minutes} min"
        if not minutes:
            return f"{hours} h"
        return f"{hours} h {minutes:02d} min"


class TripSummaryFormatter:
    separator = " to "

    def __init__(self, trip):
        self.trip = trip

    def duration(self):
        return Duration((self.trip.arrive - self.trip.depart).total_seconds())

    def render(self):
        return f"{self.trip.origin}{self.separator}{self.trip.destination}: {self.duration().format()}"


def trip_summary(trip):
    """One line for the trip list, e.g. 'Leeds to York: 1 h 05 min'."""
    return TripSummaryFormatter(trip).render()
