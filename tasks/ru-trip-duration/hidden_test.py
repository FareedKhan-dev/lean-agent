from datetime import datetime, timedelta

from _hidden_kit import check, find, load, report

models = load("trips.models")
summary = find(load("trips.summary"), "trip_summary")


def trip(seconds):
    start = datetime(2026, 5, 1, 9, 0)
    return models.Trip("Leeds", "York", start, start + timedelta(seconds=seconds), 1250)


correct = summary is not None and check("a trip over an hour", lambda: summary(trip(3900)) == "Leeds to York: 1 h 05 min")
quality = (check("under an hour reads like the rest of the site", lambda: summary(trip(2700)) == "Leeds to York: 45 min")
           and check("whole hours read like the rest of the site", lambda: summary(trip(7200)) == "Leeds to York: 2 h")
           and check("seconds round to the nearest minute", lambda: summary(trip(5380)) == "Leeds to York: 1 h 30 min"))
report(correct, quality=quality)
