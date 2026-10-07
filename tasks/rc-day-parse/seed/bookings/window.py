from bookings.dates import parse_day


def booking_window(start_text, end_text):
    """Number of nights between check-in and check-out."""
    start, end = parse_day(start_text), parse_day(end_text)
    if end <= start:
        raise ValueError("check-out must be after check-in")
    return (end - start).days
