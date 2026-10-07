from bookings.dates import parse_day


def _pad(text):
    year, month, day = text.strip().split("-")
    return f"{year}-{int(month):02d}-{int(day):02d}"


def booking_window(start_text, end_text):
    """Number of nights between check-in and check-out."""
    start, end = parse_day(_pad(start_text)), parse_day(_pad(end_text))
    if end <= start:
        raise ValueError("check-out must be after check-in")
    return (end - start).days
