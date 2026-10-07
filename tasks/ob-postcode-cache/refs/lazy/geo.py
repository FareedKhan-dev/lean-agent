import register

_last = None


def normalise(postcode):
    """'sw1a 1aa' -> 'SW1A1AA'"""
    return postcode.replace(" ", "").upper()


def lookup_district(postcode):
    """Return the district for a postcode, or None if the register does not know it."""
    global _last
    if _last is None:
        _last = register.scan(normalise(postcode))
    return _last
