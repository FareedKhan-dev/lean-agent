from fx.convert import convert


def basket_total(lines, currency):
    """Sum of (amount, currency) lines, converted into `currency`."""
    return sum(convert(amount, line_currency, currency) for amount, line_currency in lines)
