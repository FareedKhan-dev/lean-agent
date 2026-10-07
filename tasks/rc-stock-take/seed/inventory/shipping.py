from inventory import core


def dispatch(sku, qty):
    """Ship qty units straight from stock (the warehouse scanner calls this)."""
    core._take(sku, qty)
