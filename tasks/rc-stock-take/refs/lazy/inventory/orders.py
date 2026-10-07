from inventory import core


def reserve(order):
    """Reserve stock for an order: a list of (sku, qty) lines."""
    for sku, qty in order:
        if qty > core.level(sku):
            raise ValueError(f"only {core.level(sku)} of {sku} in stock")
        core._take(sku, qty)
    return True


def cancel(order):
    for sku, qty in order:
        core._put(sku, qty)
