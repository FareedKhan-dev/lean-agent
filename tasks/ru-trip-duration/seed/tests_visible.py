from datetime import datetime

from trips.models import Trip
from trips.summary import trip_summary

t = Trip("Leeds", "York", datetime(2026, 5, 1, 9, 0), datetime(2026, 5, 1, 10, 5), 1250)
assert trip_summary(t) == "Leeds to York: 1 h 05 min", trip_summary(t)
print("ok")
