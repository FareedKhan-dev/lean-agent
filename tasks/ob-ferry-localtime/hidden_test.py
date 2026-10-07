from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from _hidden_kit import check, find, load, report

timetable = load("timetable")
local = find(timetable, "local_departure")
ZONES = {"Portsmouth": "Europe/London", "Santander": "Europe/Madrid", "St John's": "America/St_Johns"}


def same(port, *ymdhm):
    utc = datetime(*ymdhm, tzinfo=timezone.utc)
    got, want = local(utc, port), utc.astimezone(ZoneInfo(ZONES[port]))
    return (got.utcoffset() == want.utcoffset()
            and got.timetuple()[:5] == want.timetuple()[:5])


summer = [("Portsmouth", 2026, 7, 1, 12, 0), ("Santander", 2026, 8, 15, 6, 30), ("St John's", 2026, 6, 20, 18, 0)]
year_round = [
    ("Portsmouth", 2026, 1, 15, 12, 0), ("Santander", 2026, 12, 1, 9, 0), ("St John's", 2026, 2, 1, 12, 0),
    ("Portsmouth", 2026, 3, 29, 0, 59), ("Portsmouth", 2026, 3, 29, 1, 0),
    ("Santander", 2026, 10, 25, 0, 59), ("Santander", 2026, 10, 25, 1, 0),
    ("St John's", 2026, 3, 8, 5, 29), ("St John's", 2026, 3, 8, 5, 30),
    ("St John's", 2026, 11, 1, 4, 29), ("St John's", 2026, 11, 1, 4, 30),
]
correct = local is not None and check("summer departures are right", lambda: all(same(*c) for c in summer))
quality = check("winter and every 2026 clock change are right", lambda: all(same(*c) for c in year_round))
report(correct, quality=quality)
