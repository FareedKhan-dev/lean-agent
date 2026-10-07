def trip_summary(trip):
    """One line for the trip list, e.g. 'Leeds to York: 1 h 05 min'."""
    minutes = int((trip.arrive - trip.depart).total_seconds() // 60)
    return f"{trip.origin} to {trip.destination}: {minutes // 60} h {minutes % 60:02d} min"
