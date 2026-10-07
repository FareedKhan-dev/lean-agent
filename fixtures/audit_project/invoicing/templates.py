FILTERS = {"money": "money", "upper": "shout"}


def money(pence):
    return f"£{pence / 100:.2f}"


def shout(text):
    return str(text).upper()


def apply(name, value):
    """Apply a named filter to a value, the way the email templates do."""
    return globals()[FILTERS[name]](value)
