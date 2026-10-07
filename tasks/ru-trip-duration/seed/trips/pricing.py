def fare(trip):
    pounds, pence = divmod(trip.price_pence, 100)
    return f"£{pounds}.{pence:02d}"
