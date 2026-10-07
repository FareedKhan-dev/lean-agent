"""Conference badges."""
from people.names import display_name


def badge_text(first, last, company):
    """The line printed on a badge, e.g. 'Ada Lovelace - Analytical Engines'."""
    return f"{display_name(first, last)} - {company}"
