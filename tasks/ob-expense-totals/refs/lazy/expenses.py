import csv
from collections import defaultdict


def totals_by_category(path):
    """Total spent per category in the expenses CSV at `path` (columns: date, category, amount)."""
    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            totals[row["category"]] += float(row["amount"])
    return dict(totals)
