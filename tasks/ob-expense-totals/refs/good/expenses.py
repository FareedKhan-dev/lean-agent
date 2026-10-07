import csv
from collections import defaultdict
from decimal import Decimal


def totals_by_category(path):
    """Total spent per category in the expenses CSV at `path` (columns: date, category, amount).
    Decimal, not float, so the totals compare exactly with the bank's figures."""
    totals = defaultdict(Decimal)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            totals[row["category"]] += Decimal(row["amount"])
    return dict(totals)
