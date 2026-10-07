from library.loans import days_late


def overdue(loans, today):
    """(title, days late) for every loan that is overdue today, most overdue first.
    `loans` is a list of (title, date borrowed)."""
    late = [(title, days_late(borrowed, today)) for title, borrowed in loans]
    return sorted([(t, d) for t, d in late if d > 0], key=lambda pair: -pair[1])
