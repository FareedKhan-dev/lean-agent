from datetime import date


def parse_day(text):
    """'2026-03-07' or '2026-3-7' -> date(2026, 3, 7)"""
    year, month, day = (int(part) for part in text.strip().split("-"))
    return date(year, month, day)
