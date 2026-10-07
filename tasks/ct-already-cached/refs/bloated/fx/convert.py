import time

from fx.rates import rate

_RATE_CACHE = {}
_TTL_S = 24 * 3600


def cached_rate(base, quote):
    """The rate, from a local cache in front of the rates service, refreshed daily."""
    hit = _RATE_CACHE.get((base, quote))
    if hit and time.monotonic() - hit[1] < _TTL_S:
        return hit[0]
    value = rate(base, quote)
    _RATE_CACHE[(base, quote)] = (value, time.monotonic())
    return value


def clear_rate_cache():
    _RATE_CACHE.clear()


def convert(amount, base, quote):
    """`amount` in minor units (pence, cents) of `base`, converted to minor units of `quote`."""
    if base == quote:
        return amount
    return round(amount * cached_rate(base, quote))
