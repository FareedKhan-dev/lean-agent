from datetime import date


def parse_day(text):
    """'2026-03-07' -> date(2026, 3, 7)"""
    return date.fromisoformat(text.strip())
