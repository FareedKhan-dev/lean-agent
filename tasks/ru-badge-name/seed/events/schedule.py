from datetime import datetime, timedelta

TALKS = [("Opening", datetime(2026, 6, 4, 9, 0), 30), ("Keynote", datetime(2026, 6, 4, 9, 30), 60)]


def ends_at(title):
    for name, start, minutes in TALKS:
        if name == title:
            return start + timedelta(minutes=minutes)
    return None
