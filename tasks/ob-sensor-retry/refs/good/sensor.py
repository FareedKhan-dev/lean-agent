import link


def parse(raw):
    """'21.5' -> 21.5; anything else is a real fault and raises ValueError."""
    return float(raw)


def read_value():
    """One temperature reading from the field sensor, retrying radio drop-outs."""
    for attempt in range(3):
        try:
            raw = link.fetch()
        except TimeoutError:
            if attempt == 2:
                raise
            continue
        return parse(raw)
