from functools import cache

import register


def normalise(postcode):
    """'sw1a 1aa' -> 'SW1A1AA'"""
    return postcode.replace(" ", "").upper()


@cache
def lookup_district(postcode):
    """Return the district for a postcode, or None if the register does not know it."""
    return register.scan(normalise(postcode))
