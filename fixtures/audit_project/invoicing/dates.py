from dateutil.parser import isoparse


def parse_issued(text):
    """The issue date of an invoice, from an ISO date string."""
    return isoparse(text).date()


def parse_issue_date(text):
    """Parse an invoice issue date."""
    return isoparse(text).date()
