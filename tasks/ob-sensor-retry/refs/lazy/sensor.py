import link


def parse(raw):
    """'21.5' -> 21.5; anything else is a real fault and raises ValueError."""
    return float(raw)


def read_value():
    """One temperature reading from the field sensor."""
    for attempt in range(3):
        try:
            return parse(link.fetch())
        except Exception:
            if attempt == 2:
                raise
