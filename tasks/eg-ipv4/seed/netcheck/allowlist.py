from netcheck.validate import is_ipv4

ALLOWED = []


def add_entry(text):
    """Save an allow-list entry typed into the admin form; refuse anything that is not an address."""
    if not is_ipv4(text):
        return False
    ALLOWED.append(text)
    return True
