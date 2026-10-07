from datetime import datetime, timezone

from timetable import local_departure

t = local_departure(datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc), "Portsmouth")
assert (t.hour, t.minute) == (13, 0), t
print("ok")
