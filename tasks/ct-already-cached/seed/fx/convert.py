from fx.rates import rate


def convert(amount, base, quote):
    """`amount` in minor units (pence, cents) of `base`, converted to minor units of `quote`."""
    if base == quote:
        return amount
    return round(amount * rate(base, quote))
