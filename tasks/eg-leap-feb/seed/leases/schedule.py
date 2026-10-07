from leases.dates import add_months


def first_payment(lease):
    """Rent is first due one month after the lease starts."""
    return add_months(lease["start"], 1)


def lease_end(lease):
    return add_months(lease["start"], 12 * lease["years"])
