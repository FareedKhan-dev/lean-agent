"""Ferry departures. Times are stored in UTC."""
from zoneinfo import ZoneInfo

PORTS = {
    "Portsmouth": "Europe/London",
    "Santander": "Europe/Madrid",
    "St John's": "America/St_Johns",
}


def local_departure(utc_time, port):
    """Return the departure as a datetime in the port's local time.
    `utc_time` is a timezone-aware datetime in UTC."""
    return utc_time.astimezone(ZoneInfo(PORTS[port]))
