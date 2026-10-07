import csv


def total_kwh(path):
    """Total kWh in the meter export CSV at `path` (columns: meter_id, kwh)."""
    with open(path, newline="", encoding="utf-8") as f:
        return sum(float(row["kwh"]) for row in csv.DictReader(f))
