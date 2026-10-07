"""Ferry departures. Times are stored in UTC."""
from datetime import datetime, timedelta, timezone

PORTS = {
    "Portsmouth": "Europe/London",
    "Santander": "Europe/Madrid",
    "St John's": "America/St_Johns",
}
RULES = {
    # port: (standard offset, summer offset, which rule)
    "Portsmouth": (0, 1, "eu"),
    "Santander": (1, 2, "eu"),
    "St John's": (-3.5, -2.5, "na"),
}


def _last_sunday(year, month):
    last = (datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)) - timedelta(days=1)
    return last - timedelta(days=(last.weekday() + 1) % 7)


def _nth_sunday(year, month, n):
    first = datetime(year, month, 1)
    first += timedelta(days=(6 - first.weekday()) % 7)
    return first + timedelta(weeks=n - 1)


class DstRule:
    """When summer time starts and ends, in UTC, for one family of rules."""

    def __init__(self, kind):
        self.kind = kind

    def window_utc(self, year, standard):
        if self.kind == "eu":   # last Sunday of March to last Sunday of October, 01:00 UTC
            start = _last_sunday(year, 3).replace(hour=1)
            end = _last_sunday(year, 10).replace(hour=1)
        else:                   # second Sunday of March to first Sunday of November, 02:00 local
            start = _nth_sunday(year, 3, 2).replace(hour=2) - timedelta(hours=standard)
            end = _nth_sunday(year, 11, 1).replace(hour=2) - timedelta(hours=standard + 1)
        return start.replace(tzinfo=timezone.utc), end.replace(tzinfo=timezone.utc)


class PortClock:
    def __init__(self, port):
        self.standard, self.summer, kind = RULES[port]
        self.rule = DstRule(kind)

    def offset(self, utc_time):
        start, end = self.rule.window_utc(utc_time.year, self.standard)
        return self.summer if start <= utc_time < end else self.standard

    def localise(self, utc_time):
        return utc_time.astimezone(timezone(timedelta(hours=self.offset(utc_time))))


def local_departure(utc_time, port):
    """Return the departure as a datetime in the port's local time.
    `utc_time` is a timezone-aware datetime in UTC."""
    return PortClock(port).localise(utc_time)
