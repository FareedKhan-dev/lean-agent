from util.timefmt import human_duration


def trip_summary(trip):
    """One line for the trip list, e.g. 'Leeds to York: 1 h 05 min'."""
    seconds = (trip.arrive - trip.depart).total_seconds()
    return f"{trip.origin} to {trip.destination}: {human_duration(seconds)}"
