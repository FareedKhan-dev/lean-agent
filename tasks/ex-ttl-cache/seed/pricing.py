from cache import TTLCache

PRICES = TTLCache(max_size=1000, ttl=300)


def supplier_price(product_id, fetch):
    """The supplier's price for a product, at most five minutes old."""
    price = PRICES.get(product_id)
    if price is None:
        price = fetch(product_id)
        PRICES.set(product_id, price)
    return price
