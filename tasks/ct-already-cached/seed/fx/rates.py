from functools import lru_cache

from fx import source


@lru_cache(maxsize=512)
def rate(base, quote):
    """How many units of `quote` one unit of `base` buys, from the rates service."""
    return source.query(base, quote)
