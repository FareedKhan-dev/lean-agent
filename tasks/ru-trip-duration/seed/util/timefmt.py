"""How durations and times are shown on the site."""


def human_duration(seconds):
    """3900 -> '1 h 05 min'; 2700 -> '45 min'; 7200 -> '2 h'. Rounds to the nearest minute."""
    minutes = round(seconds / 60)
    hours, minutes = divmod(minutes, 60)
    if not hours:
        return f"{minutes} min"
    if not minutes:
        return f"{hours} h"
    return f"{hours} h {minutes:02d} min"


def clock(dt):
    """datetime -> '09:05'"""
    return dt.strftime("%H:%M")
