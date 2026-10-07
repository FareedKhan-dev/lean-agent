from inventory import core


def low_stock(threshold=5):
    return sorted(sku for sku, qty in core.STOCK.items() if qty < threshold)
