"""Conference badges."""


def badge_text(first, last, company):
    """The line printed on a badge, e.g. 'Ada Lovelace - Analytical Engines'."""
    return f"{first.title()} {last.title()} - {company}"
