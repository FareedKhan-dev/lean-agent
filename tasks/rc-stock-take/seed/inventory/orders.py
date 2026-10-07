from inventory import core


def reserve(order):
    """Reserve stock for an order: a list of (sku, qty) lines."""
    for sku, qty in order:
        core._take(sku, qty)
    return True


def cancel(order):
    for sku, qty in order:
        core._put(sku, qty)
