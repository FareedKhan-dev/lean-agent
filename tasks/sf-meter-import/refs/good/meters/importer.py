import csv


def total_kwh(path):
    """Total kWh in the meter export CSV at `path` (columns: meter_id, kwh); bad rows are skipped."""
    total = 0.0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                total += float(row["kwh"])
            except (ValueError, TypeError, KeyError):
                continue
    return total
