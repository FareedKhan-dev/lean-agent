"""Stock levels. Every change to stock goes through this module."""

STOCK = {}


def set_stock(sku, qty):
    STOCK[sku] = qty


def level(sku):
    return STOCK.get(sku, 0)


def _take(sku, qty):
    """Remove qty units of sku from stock; refuses to go below zero."""
    if qty > level(sku):
        raise ValueError(f"only {level(sku)} of {sku} in stock, {qty} requested")
    STOCK[sku] = level(sku) - qty


def _put(sku, qty):
    STOCK[sku] = level(sku) + qty
