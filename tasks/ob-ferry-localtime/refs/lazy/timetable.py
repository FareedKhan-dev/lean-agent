"""Ferry departures. Times are stored in UTC."""
from datetime import timedelta, timezone

PORTS = {
    "Portsmouth": "Europe/London",
    "Santander": "Europe/Madrid",
    "St John's": "America/St_Johns",
}
OFFSETS = {"Portsmouth": 1, "Santander": 2, "St John's": -2.5}


def local_departure(utc_time, port):
    """Return the departure as a datetime in the port's local time.
    `utc_time` is a timezone-aware datetime in UTC."""
    return utc_time.astimezone(timezone(timedelta(hours=OFFSETS[port])))
