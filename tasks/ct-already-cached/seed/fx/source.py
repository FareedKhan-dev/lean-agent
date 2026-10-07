"""Client for the rates service. Every query is a network round trip of about 300 ms."""
RATES = {("GBP", "EUR"): 1.17, ("GBP", "USD"): 1.27, ("EUR", "GBP"): 0.855, ("USD", "GBP"): 0.787}
QUERIES = 0


def query(base, quote):
    global QUERIES
    QUERIES += 1
    return RATES[(base, quote)]
