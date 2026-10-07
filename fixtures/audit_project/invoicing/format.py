from concurrent.futures import ThreadPoolExecutor


def format_amount(pence, currency="GBP", verbose=False):
    return f"{currency} {pence / 100:.2f}"


def format_all(amounts):
    """Format many amounts at once."""
    with ThreadPoolExecutor(max_workers=8) as pool:
        return list(pool.map(format_amount, amounts))
