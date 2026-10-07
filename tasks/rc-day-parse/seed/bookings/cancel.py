from datetime import timedelta

from bookings.dates import parse_day


def cancel_deadline(checkin_text):
    """Last day a booking can be cancelled for free: two days before check-in."""
    return parse_day(checkin_text) - timedelta(days=2)
